Vue.createApp({
    data() {
        return {
            search: '',
            filter: '',
            status: 'true',
            datas: [],
            pagination: {},
            csrf: token,
            fileSelected: null,
            uploadProgress: null
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

            await axios.get(`/students/get-data?page=${page}&search=${this.search}&filter=${this.filter}&status=${this.status}`)
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
                html: 'Yakin mau hapus siswa <b>' + name + '</b>?',
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

                    await axios.post('/students/delete', {key: key}, { 
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
        onFileChange(event) {
            this.fileSelected = event.target.files[0]
            this.uploadProgress = null
        },
        async onSubmit(){
            await axios.postForm('/students/import', {file: this.fileSelected}, { 
                headers: { "X-CSRFToken": this.csrf },
                onUploadProgress: progressEvent => {
                    this.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                },
            })
            .then(response => {
                this.fileSelected = null
                this.uploadProgress = null
                $('#modalImport').modal('hide')
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
                this.fileSelected = null
                this.uploadProgress = null
                $('#modalImport').modal('hide')
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    this.getDatas(1)
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
    }
}).mount('#app')