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
                Automatic Spatial Audio Generator
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
            dark
        >
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class='text-h6'>
                        Menu
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-list>
                <v-list-item
                    v-for="item in menuItems"
                    :key="item.title"
                    @click=changeComponent(item.to)
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
            <v-container>
                <component 
                    :is=currentComponent
                    :duct='duct'
                />      
            </v-container>
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
import Resources from '@/components/pages/Resources'
import Generator from '@/components/pages/Generator'
import IrAnalysis from '@/components/pages/IrAnalysis'
import AboutThisApp from '@/components/pages/AboutThisApp'
import ducts from '@iflb/ducts-client'
export default{
    components:{
        Resources,
        Generator,
        IrAnalysis,
        AboutThisApp
    },
    data:() => ({
        duct: new ducts.Duct(),
        drawer:true,
        backgroundImage: BackgroundImage,
        currentComponent:'generator',
        menuItems:[
            { title: 'Generator', icon: 'mdi-surround-sound', to: 'generator' },
            { title: 'IRAnalysis', icon: 'mdi-sine-wave', to: 'ir-analysis' },
            { title: 'Resources', icon: 'mdi-semantic-web', to: 'resources' },
            { title: 'OpenAIR', icon: 'mdi-web-box', to: 'openair' },
            { title: 'About this app', icon: 'mdi-information', to: 'about-this-app' },
        ],
    }),
    methods:{
        changeComponent(url){
            if(url == 'openair'){
                window.open('https://www.openairlib.net/','_blank')
            }else{
                this.currentComponent = url;
                console.log(this.currentComponent)
            }
        },
        showPage(key){
            if(key == 'github'){
                window.open('https://github.com/Mtmtmtk','_blank')
            }else if(key == 'wordpress'){
                window.open('https://ms2676.wordpress.com/','_blank')
            }else if(key == 'linkedin'){
                window.open('https://www.linkedin.com/in/motoki-saito-0167931b7/','_blank')
            }
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
