<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-lg">M</span>
          </div>
          <span class="text-xl font-bold text-gray-900">MiniBlog</span>
        </router-link>
        
        <!-- Navigation principale -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link 
            to="/" 
            class="text-gray-600 hover:text-primary-600 transition-colors"
            active-class="text-primary-600 font-medium"
          >
            Accueil
          </router-link>
          <router-link 
            to="/articles" 
            class="text-gray-600 hover:text-primary-600 transition-colors"
            active-class="text-primary-600 font-medium"
          >
            Articles
          </router-link>
          <router-link 
            to="/search" 
            class="text-gray-600 hover:text-primary-600 transition-colors"
            active-class="text-primary-600 font-medium"
          >
            Recherche
          </router-link>
        </nav>
        
        <!-- Actions utilisateur -->
        <div class="flex items-center space-x-4">
          <!-- Barre de recherche mobile -->
          <button 
            @click="showMobileSearch = !showMobileSearch"
            class="md:hidden p-2 text-gray-600 hover:text-primary-600"
          >
            <Search class="w-5 h-5" />
          </button>
          
          <!-- Menu utilisateur -->
          <div v-if="authStore.isAuthenticated" class="relative">
            <button 
              @click="showUserMenu = !showUserMenu"
              class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span class="text-primary-600 font-medium text-sm">
                  {{ userInitials }}
                </span>
              </div>
              <span class="hidden sm:block text-sm font-medium text-gray-700">
                {{ authStore.user?.username }}
              </span>
              <ChevronDown class="w-4 h-4 text-gray-500" />
            </button>
            
            <!-- Menu déroulant -->
            <div 
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
            >
              <router-link 
                to="/dashboard"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                Tableau de bord
              </router-link>
              <router-link 
                to="/articles/new"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                Nouvel article
              </router-link>
              <div class="border-t border-gray-200 my-1"></div>
              <button 
                @click="logout"
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                Déconnexion
              </button>
            </div>
          </div>
          
          <!-- Boutons de connexion/inscription -->
          <div v-else class="flex items-center space-x-3">
            <router-link 
              to="/login"
              class="text-gray-600 hover:text-primary-600 font-medium"
            >
              Connexion
            </router-link>
            <router-link 
              to="/register"
              class="btn btn-primary"
            >
              Inscription
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- Barre de recherche mobile -->
      <div v-if="showMobileSearch" class="py-4 border-t border-gray-200">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher des articles..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            @keyup.enter="performSearch"
          />
          <Search class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Search, ChevronDown } from 'lucide-vue-next'

export default {
  name: 'Header',
  components: {
    Search,
    ChevronDown
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const showUserMenu = ref(false)
    const showMobileSearch = ref(false)
    const searchQuery = ref('')
    
    // Computed
    const userInitials = computed(() => {
      if (!authStore.user) return ''
      const { first_name, last_name, username } = authStore.user
      if (first_name && last_name) {
        return `${first_name[0]}${last_name[0]}`.toUpperCase()
      }
      return username[0].toUpperCase()
    })
    
    // Methods
    const logout = () => {
      authStore.logout()
      showUserMenu.value = false
      router.push('/')
    }
    
    const performSearch = () => {
      if (searchQuery.value.trim()) {
        router.push({
          name: 'Search',
          query: { q: searchQuery.value.trim() }
        })
        searchQuery.value = ''
        showMobileSearch.value = false
      }
    }
    
    // Fermer le menu utilisateur en cliquant ailleurs
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        showUserMenu.value = false
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      authStore,
      showUserMenu,
      showMobileSearch,
      searchQuery,
      userInitials,
      logout,
      performSearch
    }
  }
}
</script>
