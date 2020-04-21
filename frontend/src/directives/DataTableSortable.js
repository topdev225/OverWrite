import {Sortable} from "sortablejs";

export default {
  bind: function (el, binding) {
    let table = el.querySelector('tbody');
    Sortable.create(table, {
      handle: '[data-table-sortable-handle]',
      onEnd({newIndex, oldIndex}) {
        if (binding.value && typeof binding.value === 'function') {
          binding.value(oldIndex, newIndex)
        }
      }
    })
  }
}