<script setup>

</script>

<template>
    <div class='max-w-screen mx-auto w-full'> 
        <div class='header bg-white shadow-lg sticky top-0 z-50'>
            <div class='header-body max-w-6xl mx-auto px-4 py-3 flex items-center'> 
                <div class="text-lg font-semibold">
                    <span>BLOG</span>
                </div>
                <div class="ml-auto text-lg">
                    <span>Log in</span>
                </div>
            </div>
        </div>
        <div class="page-layout max-w-6xl mx-auto h-[calc(100vh-4rem)] flex">
            <div class="page-body flex-1">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>