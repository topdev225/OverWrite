<template>
    <v-container class="text-xs-center">
        <v-btn @click="newProduct">New product</v-btn>
        <v-btn @click="fromExisingProduct">From existing product</v-btn>
    </v-container>
</template>


<script>
export default {
    
    methods: {

        // Handlers

        newProduct () {
            this.$emit('switch-window', 2)
        }, 

        fromExisingProduct () {
            this.$emit('switch-window', 3)
        }
    }
}
</script>

