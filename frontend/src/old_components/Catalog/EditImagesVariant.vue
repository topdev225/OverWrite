<template>
  <v-layout ma-3 align-left justify-start column>
    <v-layout align-center justify-center row>
      <h2>Images</h2>
    </v-layout>
    <v-layout ma-3 align-center justify-start row>
      <v-flex ma-3 xs2 v-for="(resource, key) in resources" :key="key">
        <v-card>
          <v-img
            height="150"
            contain
            :src="'https://orderwrite-api.test-y-sbm.com/static/resources/'+ resource.uuid+'.'+resource.type"
          ></v-img>

          <v-card-actions>
            <v-btn flat color="primary" @click="deleteImage(key,resource.uuid)">Remove</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout ma-3 align-center justify-center row>
      <h2 v-show="files.length">New images</h2>
      <v-btn center class="submit-button" color="primary" v-on:click="submitFiles()" v-show="files.length > 0">
        Submit
      </v-btn>
    </v-layout>
    <v-layout ma-3>
      <v-flex xs2 offset-xs1 v-for="(file, index) in files" :key="index">
        <v-card>
          <v-img
            v-bind:ref="'preview'+parseInt( index )"
          ></v-img>

          <v-card-actions>
            <v-btn flat color="primary" @click="removeFile(index)">Remove</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <v-flex xs12 align-center justify-center row fill-height class="form">
      <form ref="fileform">
        <div class="drop-files">Drop the files here!
          <label for="file" class="submit-button v-btn theme--light primary">
            Or Click here!
          </label>
          <input class="hiden" type="file" id="file" ref="files" multiple v-on:change="handleFilesUpload()"/>
        </div>
      </form>
    </v-flex>
  </v-layout>
</template>

<script>
  import axios from '@/axios'
  /*https://orderwrite-api.test-y-sbm.com/static/resources/dcfc735b-5d4b-4e8b-bad6-aaaa09be064d.jpg*/
  export default {
    data() {
      return {
        token: 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
        dragAndDropCapable: false,
        files: [],
        resources: []
      }
    },
    mounted() {
      axios.get(`/products/variants/${this.$route.params.id}`, {
        headers: {
          'Authorization': 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
          'X-Fields': '*'
        }
      }).then(resp => {
        this.$data.resources = resp.data.resources
        console.log(resp.data)
      }).catch(err => {
        this.errors.push(err)
      })
      /*
        Determine if drag and drop functionality is capable in the browser
      */
      this.dragAndDropCapable = this.determineDragAndDropCapable();

      /*
        If drag and drop capable, then we continue to bind events to our elements.
      */
      if (this.dragAndDropCapable) {
        /*
          Listen to all of the drag events and bind an event listener to each
          for the fileform.
        */
        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(function (evt) {
          /*
            For each event add an event listener that prevents the default action
            (opening the file in the browser) and stop the propagation of the event (so
            no other elements open the file in the browser)
          */
          this.$refs.fileform.addEventListener(evt, function (e) {
            e.preventDefault();
            e.stopPropagation();
          }.bind(this), false);
        }.bind(this));

        /*
          Add an event listener for drop to the form
        */
        this.$refs.fileform.addEventListener('drop', function (e) {
          /*
            Capture the files from the drop event and add them to our local files
            array.
          */
          for (let i = 0; i < e.dataTransfer.files.length; i++) {
            this.files.push(e.dataTransfer.files[i]);
            this.getImagePreviews();
          }
        }.bind(this));
      }
    },
    methods: {
      handleFilesUpload() {
        let arr = Array.from(this.$refs.files.files)
        arr.forEach((val) => {
          this.files.push(val)
        })
        this.getImagePreviews();
      },
      determineDragAndDropCapable() {
        /*
          Create a test element to see if certain events
          are present that let us do drag and drop.
        */
        var div = document.createElement('div');

        /*
          Check to see if the `draggable` event is in the element
          or the `ondragstart` and `ondrop` events are in the element. If
          they are, then we have what we need for dragging and dropping files.

          We also check to see if the window has `FormData` and `FileReader` objects
          present so we can do our AJAX uploading
        */
        return (('draggable' in div)
          || ('ondragstart' in div && 'ondrop' in div))
          && 'FormData' in window
          && 'FileReader' in window;
      },
      getImagePreviews() {
        /*
          Iterate over all of the files and generate an image preview for each one.
        */
        for (let i = 0; i < this.files.length; i++) {
          /*
            Ensure the file is an image file
          */
          if (/\.(jpe?g|png|gif)$/i.test(this.files[i].name)) {
            /*
              Create a new FileReader object
            */
            let reader = new FileReader();

            /*
              Add an event listener for when the file has been loaded
              to update the src on the file preview.
            */
            reader.addEventListener("load", function () {
              this.$refs['preview' + parseInt(i)][0].src = reader.result;
            }.bind(this), false);

            /*
              Read the data for the file in through the reader. When it has
              been loaded, we listen to the event propagated and set the image
              src to what was loaded from the reader.
            */
            reader.readAsDataURL(this.files[i]);
          } else {
            /*
              We do the next tick so the reference is bound and we can access it.
            */
            this.$nextTick(function () {
              this.$refs['preview' + parseInt(i)][0].src = '/images/file.png';
            });
          }
        }
      },

      removeFile(key) {
        this.$data.files.splice(key, 1);
      },
      deleteImage(key, uuid) {
        axios.delete(`/data_resources/${uuid}`, {
          headers: {
            'Authorization': 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
          }
        }).then(resp => {
          console.log(resp)
          location.reload();
        }).catch(err => {
          this.errors.push(err)
        })


      },
      submitFiles() {
        for (let i = 0; i < this.files.length; i++) {
          let formData = new FormData();

          let file = this.files[i];
          formData.append('file', file);
          formData.append('meta', "{}");
          formData.append('linked_to', `product_variant:${this.$route.params.id}`);
          axios.post('/data_resources',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': this.$data.token
              }
            }
          ).then(function () {
            console.log('SUCCESS!!');
            location.reload();
          })
            .catch(function () {
              console.log('FAILURE!!');
            });
        }
      }
    }
  }
</script>
<style scoped>
  form {
  display: block;
  background: #ccc;
  margin: auto;
  margin-top: 40px;
  text-align: center;
  line-height: 400px;
  border-radius: 4px;
  }
  .hiden{
    display: none;
  }
</style>
