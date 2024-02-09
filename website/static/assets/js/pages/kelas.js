Vue.createApp({
    data() {
        return {
            search: '',
            datas: [],
            pagination: {},
            csrf: token,
            selectedData: {
                id: '',
                angka: '',
                rombel: '',
                romawi: '',
                siswa: ''
            }
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.getDatas(1)
    },
    methods: {
        async getDatas(page){
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

            await axios.get(`/class/get-data?page=${page}&search=${this.search}`)
                .then((result) => {
                    $.unblockUI();

                    var data = JSON.parse(result.data)
                    this.datas = data.data
                    this.pagination = data.pagination
                })
                .catch(() => {
                    $.unblockUI();
                    
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        },
        async deleteData(key, name){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau hapus kelas <b>' + name + '</b>?',
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

                    await axios.post('/class/delete', {key: key}, { 
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
                            this.getDatas(1)
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
        openModal(index){
            this.selectedData = {...this.datas[index]}
            $('#modalUbah').modal('show')
        },
        async onUpdate(){
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

            await axios.post('/class/edit', this.selectedData, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                $('#modalUbah').modal('hide')
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    this.getDatas(1)
                })
            })
            .catch(error => {
                $.unblockUI();
                $('#modalUbah').modal('hide')
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        },
        nextPage(){
            if(this.pagination.has_next){
                this.getDatas(this.pagination.current_page_number + 1)
            }
        },
        previousPage(){
            if(this.pagination.has_previous){
                this.getDatas(this.pagination.current_page_number - 1)
            }
        },
        async onUpgrade(key, name){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau naikan semua siswa di kelas <b>' + name + '</b>?',
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

                    await axios.post('/class/upgrade', {key: key}, { 
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
                            this.getDatas(1)
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