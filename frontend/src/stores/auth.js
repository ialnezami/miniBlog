import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const isLoading = ref(false)
  
  const toast = useToast()
  
  // Computed properties
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_staff || false)
  
  // Actions
  const login = async (credentials) => {
    try {
      isLoading.value = true
      
      const response = await api.post('/auth/login/', credentials)
      const { access, refresh, user: userData } = response.data
      
      // Stocker les tokens
      token.value = access
      refreshToken.value = refresh
      user.value = userData
      
      // Sauvegarder en localStorage
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)
      
      // Configurer le token pour les futures requêtes
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      toast.success('Connexion réussie !')
      return { success: true }
      
    } catch (error) {
      const message = error.response?.data?.detail || 'Erreur de connexion'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const register = async (userData) => {
    try {
      isLoading.value = true
      
      const response = await api.post('/auth/register/', userData)
      
      toast.success('Inscription réussie ! Vous pouvez maintenant vous connecter.')
      return { success: true }
      
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur d\'inscription'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = () => {
    // Nettoyer les tokens
    token.value = null
    refreshToken.value = null
    user.value = null
    
    // Nettoyer le localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    
    // Nettoyer les headers API
    delete api.defaults.headers.common['Authorization']
    
    toast.success('Déconnexion réussie')
  }
  
  const refreshAuth = async () => {
    if (!refreshToken.value) {
      logout()
      return false
    }
    
    try {
      const response = await api.post('/auth/refresh/', {
        refresh: refreshToken.value
      })
      
      const { access } = response.data
      token.value = access
      localStorage.setItem('token', access)
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      return true
      
    } catch (error) {
      console.error('Erreur lors du refresh du token:', error)
      logout()
      return false
    }
  }
  
  const fetchProfile = async () => {
    if (!token.value) return false
    
    try {
      const response = await api.get('/auth/profile/')
      user.value = response.data
      return true
    } catch (error) {
      console.error('Erreur lors de la récupération du profil:', error)
      return false
    }
  }
  
  const updateProfile = async (profileData) => {
    try {
      isLoading.value = true
      
      const response = await api.put('/auth/profile/', profileData)
      user.value = response.data
      
      toast.success('Profil mis à jour avec succès !')
      return { success: true }
      
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur lors de la mise à jour'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Initialisation
  const init = async () => {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      await fetchProfile()
    }
  }
  
  return {
    // State
    user,
    token,
    refreshToken,
    isLoading,
    
    // Computed
    isAuthenticated,
    isAdmin,
    
    // Actions
    login,
    register,
    logout,
    refreshAuth,
    fetchProfile,
    updateProfile,
    init
  }
})
