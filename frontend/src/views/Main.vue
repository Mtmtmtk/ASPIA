<template>
    <div>
        <v-app-bar
            app
            fixed
            dark
            :src=backgroundImage
        >
            <template v-slot:img='{props}'>
                <v-img
                    v-bind='props'
                    gradient="to top right, rgb(129,175,179,.7), rgb(120,144,156,.61)"
                />
            </template>
            <v-app-bar-nav-icon @click='drawer = !drawer'/>
            <v-app-bar-title>
                Multi Signal Processing Tool
            </v-app-bar-title>
            <v-spacer />
            <v-btn 
                icon
                @click='showPage("github")'
            >
                <v-icon>mdi-github</v-icon>
            </v-btn>
            <v-btn 
                icon
                @click='showPage("wordpress")'
            >
                <v-icon>mdi-wordpress</v-icon>
            </v-btn>
            <v-btn 
                icon
                @click='showPage("linkedin")'
            >
                <v-icon>mdi-linkedin</v-icon>
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer 
            app
            v-model='drawer' 
            color='#37474F'
            width='210'
            dark
        >
            <v-list>
                <v-list-item
                    v-for="item in menuItems"
                    :key="item.title"
                    :to='item.to'
                >
                    <v-list-item-icon>
                        <v-icon>{{item.icon}}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{item.title}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
            <v-divider />

            <template v-slot:prepend>
                <v-list>
                    <v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class='text-h6'>
                                Menu
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-divider />
                    <v-list-item>
                        <v-list-item-content>
                                <v-card
                                    flat
                                    tile
                                    :ripple='false'
                                    @click='showPage("openair")'
                                >
                                    <v-img
                                        class='d-flex justify-start'
                                        max-height='30'
                                        :src="require('@/assets/img/openair.png')"
                                        contain
                                    >
                                    </v-img>
                                </v-card>
                        </v-list-item-content>
                    </v-list-item>
                    <v-divider/>
                </v-list>
            </template>
            <template v-slot:append>
                <v-list>
                    <v-list-item @click="closeMenu">
                        <v-list-item-icon>
                            <v-icon>mdi-chevron-left</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Close Menu</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </template>

        </v-navigation-drawer>
        <v-main app>
            <router-view
                :duct='duct'
            />
        </v-main>
        <v-footer app dark>
            <v-col class='text-center' >
                {{new Date().getFullYear()}} - <strong>Motoki Saito, University of York</strong>
            </v-col>
        </v-footer>
    </div>
</template>
<script>
import BackgroundImage from '@/assets/img/JackLyons.jpg'
import ducts from '@iflb/ducts-client'
export default{
    data:() => ({
        duct: new ducts.Duct(),
        drawer:true,
        backgroundImage: BackgroundImage,
        menuItems:[
            { title: 'Generator', icon: 'mdi-surround-sound', to: '/main/generator' },
            { title: 'IRAnalysis', icon: 'mdi-sine-wave', to: '/main/ir-analysis' },
            { title: 'Theory', icon: 'mdi-calculator-variant-outline', to: '/main/theory' },
            { title: 'Resources', icon: 'mdi-semantic-web', to: '/main/resources' },
            { title: 'About this app', icon: 'mdi-information', to: '/main/about-this-app' },
        ],
    }),
    methods:{
        showPage(key){
            if(key == 'github') window.open('https://github.com/Mtmtmtk','_blank');
            else if(key == 'wordpress') window.open('https://ms2676.wordpress.com/','_blank');
            else if(key == 'linkedin') window.open('https://www.linkedin.com/in/motoki-saito-0167931b7/','_blank');
            else if(key == 'openair') window.open('https://www.openairlib.net/','_blank');
        },
        closeMenu(){
            this.drawer = false;
        }
    },
    created(){
        this.duct.open("/ducts/wsd");
    }
}
</script>
