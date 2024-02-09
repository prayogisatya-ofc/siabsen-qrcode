Vue.createApp({
    data() {
        return {
            form: {
                id: '',
                kelas: '',
                tanggal: '',
            },
            detailAbsensi: [],
            csrf: token,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.form.id = urlPats[urlPats.length - 2]

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

            await axios.get(`/presences/${this.form.id}/get-detail`)
                .then((result) => {
                    $.unblockUI()
                    var data = result.data
                    this.form.kelas = data.kelas
                    this.form.tanggal = data.tanggal
                    this.form.deskripsi = data.deskripsi
                    this.detailAbsensi = data.detail
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
        async deleteData(key, kelas, tanggal){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau hapus absen kelas <b>' + kelas + '</b> pada <b>' + tanggal + '</b>?',
                showCancelButton: true,
                confirmButtonText: "Yakin",
                cancelButtonText: "Batal",
            }).then( async (result) => {
                if (result.isConfirmed) {
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

                    await axios.post('/presences/delete', {key: key}, { 
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
                            location.href = '/presences'
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
                }
            })
        },
    }
}).mount('#app')