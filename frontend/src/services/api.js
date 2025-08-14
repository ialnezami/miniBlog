import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Configuration de base d'Axios
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // Si l'erreur est 401 et qu'on n'a pas déjà tenté de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const authStore = useAuthStore()
      
      try {
        // Tenter de rafraîchir le token
        const success = await authStore.refreshAuth()
        
        if (success) {
          // Retenter la requête originale avec le nouveau token
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Si le refresh échoue, rediriger vers la connexion
        authStore.logout()
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// Service pour les articles
export const articlesService = {
  // Récupérer tous les articles
  getAll: (params) => api.get('/articles/', { params }),
  
  // Récupérer un article par slug
  getBySlug: (slug) => api.get(`/articles/${slug}/`),
  
  // Créer un article
  create: (data) => api.post('/articles/', data),
  
  // Mettre à jour un article
  update: (id, data) => api.put(`/articles/${id}/`, data),
  
  // Supprimer un article
  delete: (id) => api.delete(`/articles/${id}/`),
  
  // Publier un article
  publish: (id) => api.post(`/articles/${id}/publish/`),
  
  // Vérifier avec l'IA
  checkWithAI: (id) => api.post(`/articles/${id}/check_with_ai/`),
  
  // Rechercher des articles
  search: (data) => api.post('/articles/search/', data),
  
  // Mes articles
  getMyArticles: () => api.get('/articles/my_articles/'),
  
  // Mes brouillons
  getDrafts: () => api.get('/articles/drafts/'),
}

// Service pour les catégories
export const categoriesService = {
  getAll: () => api.get('/categories/'),
  getBySlug: (slug) => api.get(`/categories/${slug}/`),
}

// Service pour les tags
export const tagsService = {
  getAll: () => api.get('/tags/'),
  getBySlug: (slug) => api.get(`/tags/${slug}/`),
}

// Service pour les commentaires
export const commentsService = {
  getAll: (params) => api.get('/comments/', { params }),
  create: (data) => api.post('/comments/', data),
  update: (id, data) => api.put(`/comments/${id}/`, data),
  delete: (id) => api.delete(`/comments/${id}/`),
}

// Service pour l'authentification
export const authService = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  refresh: (refreshToken) => api.post('/auth/refresh/', { refresh: refreshToken }),
  verify: (token) => api.post('/auth/verify/', { token }),
  profile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.put('/auth/profile/', data),
}

// Service pour la vérification IA
export const aiService = {
  checkArticle: (data) => api.post('/ai/check-article/', data),
  checkAppropriate: (data) => api.post('/ai/check-appropriate/', data),
  suggestImprovements: (data) => api.post('/ai/suggest-improvements/', data),
}

export default api
