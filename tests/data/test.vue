<template>
    <div class="Button">
        /* ... */
    </div>
</template>

<script>
  /**
   * The only true button.
   */
export default {
    name: 'Button',
    props: {
        /**
       * The color for the button.
       */
        color: {
            type: String,
            default: '#333'
        },
        /**
       * The size of the button
       */
        size: {
            type: String,
            default: 'normal'
        },
        /**
       * Gets called when the user clicks on the button
       */
        onClick: {
            type: Function,
            default: (event) => {
                console.log('You have clicked me!', event.target)
            }
        }
    }
    /* ... */
}
</script>