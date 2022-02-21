export const encodeWAV = function(samples,samplingRate, _channels, _blockSize){
        const _buffer = new ArrayBuffer(44 + samples.length*2);
        let _view = new DataView(_buffer);
        const writeString = function(view, offset, str){
            for(let i=0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
        }
        const floatTo16BitPCM = function(output, offset, input){
            for(let i=0; i < input.length; i++, offset +=2){
                let s = Math.max(-1, Math.min(1, input[i]));
                output.setInt16(offset, s<0 ? s*0x8000 : s*0x7FFF, true);
            }
        }
        const _fileSize = 44 + samples.length*2 - 8;

        writeString(_view, 0, 'RIFF');//riff識別
        _view.setUint32(4, _fileSize, true);//chunk size
        writeString(_view, 8, 'WAVE')//format
        writeString(_view,12, 'fmt ');//fmt識別子(最後にスペース開けるのめっちゃ大事)
        _view.setUint32(16, 16, true);//fmt chunk's byte
        _view.setUint16(20,  1, true);//sound format: 1 means non-compressed linear PCM format
        _view.setUint16(22,  _channels, true);//channel(s) one or two
        _view.setUint32(24, samplingRate  , true);//sampling rate
        _view.setUint32(28, samplingRate*_blockSize, true);//sampling rate * block size
        _view.setUint16(32, _blockSize, true);//block size: channel(s) * bit/8
        _view.setUint16(34, 16, true);//bit per sample
        writeString(_view, 36, 'data');
        _view.setUint32(40, samples.length*2, true);
        floatTo16BitPCM(_view, 44, samples);
        return _view
}
