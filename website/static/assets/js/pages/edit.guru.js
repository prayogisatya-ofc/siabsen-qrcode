Vue.createApp({
    data() {
        return {
            form: {
                id: '',
                nama: '',
                kode: '',
                status: '',
                foto: null
            },
            csrf: token,
            showPassword: false,
            fotoPreview: null
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.form.id = urlPats[urlPats.length - 1]

        this.getDetail()
    },
    methods: {
        async getDetail(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                    backgroundColor: 'transparent',
                    border: '0'
                },
                overlayCSS: {
                    opacity: 0.5
                }
            })

            await axios.get(`/teachers/${this.form.id}/get-detail`)
                .then((result) => {
                    $.unblockUI()
                    var data = result.data
                    this.form.nama = data.nama
                    this.form.kode = data.kode
                    this.form.status = data.status
                    this.form.foto = data.foto
                    this.fotoPreview = data.foto
                })
                .catch(() => {
                    $.unblockUI()
                    Swal.fire({
                        icon: "warning",
                        text: error.response.data.error,
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        },
        async onSubmit(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                    backgroundColor: 'transparent',
                    border: '0'
                },
                overlayCSS: {
                    opacity: 0.5
                }
            })

            await axios.postForm(`/teachers/${this.form.id}/submit`, this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    location.href = "/teachers"
                })
            })
            .catch(error => {
                $.unblockUI()
                Swal.fire({
                    icon: "warning",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        },
        onFileChange(event) {
            this.form.foto = event.target.files[0]
            if(this.form.foto){
                const reader = new FileReader()
                reader.onload = (e) => {
                    this.fotoPreview = e.target.result
                }
                reader.readAsDataURL(this.form.foto)
            }
        },
    }
}).mount('#app')