<template>
    <i class="feed-sidebar-toggler fa fa-bars" aria-hidden="true" @click.prevent="toggle">
    </i>
</template>

<script>
export default {
    name: "SidebarToggler",
    data() {
        return {
            isShown: false,
        };
    },
    created() {
      document.getElementById("app").classList.add('has-mobile-menu');
    },
    methods: {
        toggle() {
            this.isShown = !this.isShown;
            document.getElementById("app").classList.toggle("mobile-menu-opened", this.isShown);
            document.querySelector(".feed-main").classList.toggle("feed-main-closed", this.isShown);
        },
    },
};
</script>
