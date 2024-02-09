Vue.createApp({
    data() {
        return {
            form: {
                username: '',
                password: ''
            },
            csrf: token,
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

            await axios.post('/auth/login/authenticate', this.form, { 
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
                    var url_string = window.location.href;
                    var url = new URL(url_string);
                    if (url.searchParams.has("next")) {
                        var nextUrl = url.searchParams.get("next")
                        window.location.href = nextUrl
                    } else {
                        window.location.href = "/"
                    }
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
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        }
    },
    computed: {
        passwordFieldType() {
          return this.showPassword ? 'text' : 'password';
        },
        toggleButtonIcon() {
            return this.showPassword ? 'ti-eye' : 'ti-eye-off';
        }
    }
}).mount('#app')