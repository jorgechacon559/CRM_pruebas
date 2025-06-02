import { defineStore } from 'pinia'
export const useMessageStore = defineStore('message', {
  state: () => ({
    msg: '',
    type: 'success'
  }),
  actions: {
    setMessage(msg, type = 'success') {
      this.msg = msg
      this.type = type
    },
    clearMessage() {
      this.msg = ''
      this.type = 'success'
    }
  }
})