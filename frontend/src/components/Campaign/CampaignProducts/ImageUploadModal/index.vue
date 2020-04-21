<template>
  <v-dialog
    v-model="imageUploadModalEnabled"
    persistent
    scrollable
    max-width="800">

    <v-card>
      <v-card-title primary-title class="headline">{{$props.title}}</v-card-title>

      <v-divider></v-divider>

      <v-card-text class="text-xs-center">
        <img :src="imageUrl" height="250" v-if="imageUrl"/>
        <v-text-field label="Select Image" @click='pickFile' v-model='imageName'
                      prepend-icon='attach_file'></v-text-field>
        <input
          type="file"
          style="display: none"
          ref="image"
          accept="image/*"
          @change="onFilePicked">
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn :disabled="!imageFile" color="primary" @click="save">save</v-btn>
        <v-btn color="error" @click="disable">cancel</v-btn>
      </v-card-actions>
    </v-card>

  </v-dialog>
</template>


<script>

    import axios from '@/axios'

    export default {

        props: [
            'title'
        ],

        data() {
            return {
                imageUploadModalEnabled: false,

                imageName: '',
                imageUrl: '',
                imageFile: '',

                meta: null
            }
        },

        methods: {

            // Modal events
            enable(meta) {
                this.$data.meta = meta
                this.$data.imageUploadModalEnabled = true
            },

            disable() {
                this.imageName = ''
                this.imageFile = ''
                this.imageUrl = ''
                this.$data.imageUploadModalEnabled = false
            },

            // Internal methods

            pickFile() {
                this.$refs.image.click()
            },

            onFilePicked(e) {
                const files = e.target.files
                if (files[0] !== undefined) {
                    this.imageName = files[0].name
                    if (this.imageName.lastIndexOf('.') <= 0) {
                        return
                    }
                    const fr = new FileReader()
                    fr.readAsDataURL(files[0])
                    fr.addEventListener('load', () => {
                        this.$data.imageUrl = fr.result
                        this.$data.imageFile = files[0] // this is an image file that can be sent to server...
                    })
                } else {
                    this.$data.imageName = ''
                    this.$data.imageFile = ''
                    this.$data.imageUrl = ''
                }
            },

            save() {
                // Prepare params
                let params = {
                    headers: {
                        'Authorization': this.$store.state.token,
                        'Content-Type': 'multipart/form-data'
                    }
                }
                let url = 'resources'
                let _meta = JSON.stringify({})
                let formData = new FormData()
                formData.append('file', this.$data.imageFile)
                formData.append('meta', _meta)
                formData.append('linked_to', Math.random().toString(36).substring(7))
                // Upload
                axios.post(url, formData, params).then(resp => {
                    this.$emit('save', resp.data, this.$data.meta)
                    this.disable()
                }).catch(err => {
                    this.$store.dispatch('raiseError', err)
                })
            }
        }

    }
</script>
