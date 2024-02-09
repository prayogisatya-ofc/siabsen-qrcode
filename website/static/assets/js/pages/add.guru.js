Vue.createApp({
    data() {
        return {
            form: {
                nama: '',
                kode: '',
                status: '',
                foto: null
            },
            csrf: token,
            fotoPreview: null
        }
    },
    delimiters: ['[[', ']]'],
    methods: {
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

            await axios.postForm('/teachers/add/submit', this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI();
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
                $.unblockUI();
                Swal.fire({
                    icon: "error",
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