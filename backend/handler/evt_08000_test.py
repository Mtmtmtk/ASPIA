from ducts.spi import EventHandler
import io
import pickle
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_get_content = manager.get_handler_module('BLOBS').get_content
        self.evt_list_groups = manager.get_handler_module('BLOBS_GROUP_LIST_NAMES').list_groups
        self.evt_add_group = manager.get_handler_module('BLOBS_GROUP_ADD').add_group
        self.evt_exists_group = manager.get_handler_module('BLOBS_GROUP_EXISTS').get_metadata
        self.evt_add_content = manager.get_handler_module('BLOBS_CONTENT_ADD').add_content
        self.evt_exists_content = manager.get_handler_module('BLOBS_CONTENT_EXISTS').get_metadata
        self.evt_update_content = manager.get_handler_module('BLOBS_CONTENT_UPDATE').update_content
        self.evt_list_contents = manager.get_handler_module('BLOBS_CONTENT_LIST').list_contents
        self.evt_get_content_metadata = manager.get_handler_module('BLOBS_CONTENT_METADATA').get_metadata
        self.evt_list_content_versions = manager.get_handler_module('BLOBS_CONTENT_VERSIONS').list_versions
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, frame_no: int, group_key: str, data: list, mode: str):
        if(mode == 'save'):
            np_data = np.array(data)
            if len(data) == 1:
                np_data = np_data.flatten()
            df = pd.DataFrame(np_data.T)
            await self.save_dataframe_by_frame(frame_no, group_key, df, 'pkl')
            return {}
        elif(mode == 'load'):
            concat_df = pd.DataFrame(index=[])
            for idx in range(frame_no):
                ret_df = await self.load_dataframe_by_frame(idx, group_key, '', 'pkl')
                concat_df = pd.concat([concat_df,ret_df])
            concat_df = concat_df.reset_index(drop=True)
            print(concat_df)
            return concat_df.values.tolist()

    async def content_key_by_frame(self, frame_no: int):
        return f'frame_no_{frame_no:02}'

    async def save_dataframe_by_frame(self, frame_no: int, group_key: str, df: pd.DataFrame, namespace: str=''):
        content = pickle.dumps(df)
        return await self.save_bytes_by_frame(frame_no, group_key, content, namespace)

    async def save_bytes_by_frame(self, frame_no: int, group_key: str, content: bytes, namespace: str=''):
        if not (await self.evt_exists_group(group_key, namespace)):
            await self.evt_add_group(group_key, namespace)

        content_key = await self.content_key_by_frame(frame_no)
        content_exists = await self.evt_exists_content(group_key, content_key, namespace)
        func = self.evt_update_content if content_exists else self.evt_add_content
        return await func(
            group_key=group_key,
            content=content,
            content_key=content_key,
            namespace=namespace
        )

    async def load_binary(self, group_key: str, content_key: str, version: str='', namespace: str=''):
        gen = self.evt_get_content(
            group_key=group_key,
            content_key=content_key,
            version=version,
            namespace=namespace
        )
        metadata, length = await gen.__anext__()
        data = b''
        async for ret in gen:
            data += ret
            if len(data)>=length: break
        return data

    async def load_binary_by_frame(self, frame_no: int, group_key: str, version: str='', namespace: str=''):
        content_key = await self.content_key_by_frame(frame_no)
        return await self.load_binary(
            group_key=group_key,
            content_key=content_key,
            version=version,
            namespace=namespace
        )

    async def load_dataframe_by_frame(self, frame_no: int, group_key: str, version: str='', namespace: str=''):
        data = await self.load_binary_by_frame(frame_no, group_key, version, namespace)
        return pd.read_pickle(io.BytesIO(data))

