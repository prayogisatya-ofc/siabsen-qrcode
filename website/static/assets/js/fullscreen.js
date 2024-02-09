Vue.createApp({
    data() {
        return {
            isFullScreen: false
        }
    },
    delimiters: ['[[', ']]'],
    methods: {
        toggleFullScreen(){
            this.isFullScreen = !this.isFullScreen

            if(this.isFullScreen){
                document.documentElement.requestFullscreen()
            } else {
                document.exitFullscreen()
            }
        }
    }
}).mount('#full')