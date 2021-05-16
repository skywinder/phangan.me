<template>
    <li @click="copyInvite">
        <label class="copy-invite-item">
            <input type="text" :value="inviteUrl" ref="input" readonly>
            <button class="button" title="Копировать адрес инвайта">
                Copy
            </button>
        </label>
    </li>
</template>

<script>
export default {
    name: "UserInvite",
    props: {
        url: {
            type: String,
            default: '',
            required: true,
        },
        days: {
            type: Number,
            default: 0,
            required: true,
        },
    },
    data() {
        return {
            inviteUrl: window.location.origin + this.url,
            inviteDays: this.days || '',
        };
    },
    methods: {
        copyInvite() {
            this.$refs.input.select();
            document.execCommand('copy');
        },
    },
};
</script>
