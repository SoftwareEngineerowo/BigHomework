import { ref} from 'vue'
import { defineStore } from 'pinia'

export const useActiveStore = defineStore('active', () => {
    const activePath = ref(0)
    const updateActiveWeb = (a)=>{
      activePath.value = a
    }
    return { activePath, updateActiveWeb }
},
{
  persist: true
}
)
