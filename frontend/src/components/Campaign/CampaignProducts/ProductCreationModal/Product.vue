<template>

    <div>
        <v-form
                ref="productForm"
                v-model="productFormValid">
            <v-text-field
                    v-model="name"
                    label="Product Name *"
                    counter="60"
                    :rules="[validateCharLimit(60)]">
            </v-text-field>
            <v-tooltip top>
                <v-text-field
                        v-model="itemNumber"
                        label="Item number"
                        slot="activator"
                >
                </v-text-field>
                <span>Vendor's published SKU number</span>
            </v-tooltip>
            <v-select
                    :disabled="editing"
                    v-model="productTypeID"
                    :items="productTypesByCampaign"
                    item-text="name"
                    item-value="id"
                    label="Product type *">
            </v-select>

        </v-form>

    </div>

</template>


<script>

    import axios from '@/axios'
    import ImageUploadModal from '../ImageUploadModal'

    import rules from '@/mixins/rules'

    export default {

        props: [
            'productTypes'
        ],

        mixins: [
            rules
        ],

        components: {
            'image-upload-modal': ImageUploadModal
        },

        data() {
            return {
                productFormValid: null,
                editing: false,

                name: '',
                itemNumber: '',
                productTypeID: null,

                imageName: '',
                imageFile: '',

                resources: [],

                product: {},
            }
        },

        computed: {
            productTypesByCampaign() {
                if (!this.productTypes) {
                    return [];
                } else {
                    return this.productTypes;
                }
            },
            nextButtonDisabled() {
                let disabled = true
                if (this.$data.name && this.$data.productTypeID && this.$data.productFormValid)
                    disabled = false
                return disabled
            },
            imageURL() {
                if (!this.resources.length)
                    return null
                return `${process.env.API_BASE_URL}` +
                    `/static` +
                    `/resources` +
                    `/${this.resources[0].uuid}` +
                    `.${this.resources[0].type}`
            }
        },

        methods: {
            // Load product for editing
            load(product) {
                this.editing = true
                this.name = product.name
                this.itemNumber = product.item_number
                this.productTypeID = product.product_type_id
                this.resources = product.resources
                this.product = product;
            },
            drop() {
                this.name = ''
                this.itemNumber = ''
                this.productTypeID = null
                this.resources = []
            },
            // Add product and proceed to next step
            next() {
                this.$emit('add-product', {
                    'name': this.$data.name,
                    'item_number': this.$data.itemNumber,
                    'product_type_id': this.$data.productTypeID,
                    'distributor_id': this.$store.state.campaign.distributor.id,
                    'product_variants': [],
                    'resources': this.resources
                })
                this.$emit('show-options')
            },

            // Image
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
                        this.$data.imageFile = files[0] // this is an image file that can be sent to server...
                    })
                } else {
                    this.$data.imageName = ''
                    this.$data.imageFile = ''
                    this.$data.imageUrl = ''
                }
                setTimeout(this._upload, 500)
            },
            _upload() {
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
                    this.resources = [resp.data]
                }).catch(err => {
                    this.$store.dispatch('raiseError', err)
                })
            }
        }

    }
</script>
