
export default {
    methods: {
        formatCurrency (val) {
            return parseFloat(Math.round(val * 100) / 100).toFixed(2);
        }
    }
}