import { ref} from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref({})
  const updateUserInfo = (obj)=>{
    console.log("更新用户信息")
    userInfo.value = obj
  }

  return { userInfo , updateUserInfo }
},
{
  persist: true
}
)
