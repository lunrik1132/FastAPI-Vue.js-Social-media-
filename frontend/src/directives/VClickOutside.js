export const vClickOutside = {
    mounted(el, binding) {
        el.clickOutside = event => {
            if (!(el === event.target || el.contains(event.target))) {
                binding.value(event)
            }
        }
        document.addEventListener('click', el.clickOutside)
    },
    unmounted(el) {
        document.removeEventListener('click', el.clickOutside)
    }
}