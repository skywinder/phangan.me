<template>
    <label class="copy-bot-code" @click="copyCode">
        <input type="text" :value="code" ref="input" readonly>
        <button class="button" title="Копировать секретный код">
            Copy
        </button>
    </label>
</template>

<script>
export default {
    name: "BotAuthCode",
    props: {
        code: {
            type: String,
            default: '',
            required: true,
        },
    },
    methods: {
        copyCode(e) {
            this.$refs.input.select();
            document.execCommand('copy');
            e.preventDefault();
        },
    },
};
</script>
