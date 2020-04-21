/* TODO: Resource mixin prototype.*/
export default {
  methods: {
    async loadResources(options = { name: 'data' }) {
      const { name: n } = options;
      this[n].pending = true;
      const { data } = await this.$axios.get(options.path, options.params);
      this[n].data = data;
      this[n].pending = false;
      return data;
    },
    async loadSingleResource(options = { name: 'data' }) {
      const { name: n } = options;
      this[n].pending = true;
      const { data } = await this.$axios.get(options.path + '/' + options.id, options.params);
      this[n].item = data;
      this[n].pending = false;
      return data;
    },
    async submitResource(options = { name: 'data', item: {} }) {
      const { name: n, item } = options;
      this[n].pending = true;
      const method = item.id ? 'put' : 'post';
      const { data } = await this.$axios[method](options.path + (item.id ? '/' + item.id : ''), options.params);
      this[n].pending = false;
      return data;
    },
    async removeResource(options = { name: 'data' }) {
      const { name: n } = options;
      this[n].pending = true;
      await this.$axios.delete(options.path + '/' + options.id, options.params);
      this[n].pending = false;
    }
  }
}
