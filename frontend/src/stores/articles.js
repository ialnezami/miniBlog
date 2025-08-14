import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'

export const useArticlesStore = defineStore('articles', () => {
  const articles = ref([])
  const currentArticle = ref(null)
  const categories = ref([])
  const tags = ref([])
  const isLoading = ref(false)
  const totalPages = ref(1)
  const currentPage = ref(1)
  
  const toast = useToast()
  
  // Computed properties
  const publishedArticles = computed(() => 
    articles.value.filter(article => article.status === 'published')
  )
  
  const draftArticles = computed(() => 
    articles.value.filter(article => article.status === 'draft')
  )
  
  // Actions
  const fetchArticles = async (page = 1, filters = {}) => {
    try {
      isLoading.value = true
      
      const params = { page, ...filters }
      const response = await api.get('/articles/', { params })
      
      articles.value = response.data.results || response.data
      currentPage.value = page
      
      if (response.data.count) {
        totalPages.value = Math.ceil(response.data.count / 10) // 10 articles par page
      }
      
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la récupération des articles'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchArticle = async (slug) => {
    try {
      isLoading.value = true
      
      const response = await api.get(`/articles/${slug}/`)
      currentArticle.value = response.data
      
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la récupération de l\'article'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const createArticle = async (articleData) => {
    try {
      isLoading.value = true
      
      const response = await api.post('/articles/', articleData)
      const newArticle = response.data
      
      articles.value.unshift(newArticle)
      toast.success('Article créé avec succès !')
      
      return { success: true, article: newArticle }
      
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur lors de la création'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const updateArticle = async (id, articleData) => {
    try {
      isLoading.value = true
      
      const response = await api.put(`/articles/${id}/`, articleData)
      const updatedArticle = response.data
      
      // Mettre à jour dans la liste
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index] = updatedArticle
      }
      
      // Mettre à jour l'article courant si c'est le même
      if (currentArticle.value?.id === id) {
        currentArticle.value = updatedArticle
      }
      
      toast.success('Article mis à jour avec succès !')
      return { success: true, article: updatedArticle }
      
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur lors de la mise à jour'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const deleteArticle = async (id) => {
    try {
      isLoading.value = true
      
      await api.delete(`/articles/${id}/`)
      
      // Supprimer de la liste
      articles.value = articles.value.filter(a => a.id !== id)
      
      // Nettoyer l'article courant si c'est le même
      if (currentArticle.value?.id === id) {
        currentArticle.value = null
      }
      
      toast.success('Article supprimé avec succès !')
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la suppression'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const publishArticle = async (id) => {
    try {
      isLoading.value = true
      
      const response = await api.post(`/articles/${id}/publish/`)
      const publishedArticle = response.data.article
      
      // Mettre à jour dans la liste
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index] = publishedArticle
      }
      
      // Mettre à jour l'article courant si c'est le même
      if (currentArticle.value?.id === id) {
        currentArticle.value = publishedArticle
      }
      
      toast.success('Article publié avec succès !')
      return { success: true, article: publishedArticle }
      
    } catch (error) {
      const message = 'Erreur lors de la publication'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const checkWithAI = async (id) => {
    try {
      isLoading.value = true
      
      const response = await api.post(`/articles/${id}/check_with_ai/`)
      const result = response.data
      
      // Mettre à jour l'article avec les résultats de l'IA
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index] = result.article
      }
      
      if (currentArticle.value?.id === id) {
        currentArticle.value = result.article
      }
      
      toast.success('Article vérifié avec l\'IA !')
      return { success: true, result }
      
    } catch (error) {
      const message = 'Erreur lors de la vérification IA'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const searchArticles = async (searchData) => {
    try {
      isLoading.value = true
      
      const response = await api.post('/articles/search/', searchData)
      articles.value = response.data
      
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la recherche'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories/')
      categories.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des catégories:', error)
    }
  }
  
  const fetchTags = async () => {
    try {
      const response = await api.get('/tags/')
      tags.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des tags:', error)
    }
  }
  
  const fetchMyArticles = async () => {
    try {
      isLoading.value = true
      
      const response = await api.get('/articles/my_articles/')
      articles.value = response.data
      
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la récupération de vos articles'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchDrafts = async () => {
    try {
      isLoading.value = true
      
      const response = await api.get('/articles/drafts/')
      articles.value = response.data
      
      return { success: true }
      
    } catch (error) {
      const message = 'Erreur lors de la récupération des brouillons'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Initialisation
  const init = async () => {
    await Promise.all([
      fetchCategories(),
      fetchTags()
    ])
  }
  
  return {
    // State
    articles,
    currentArticle,
    categories,
    tags,
    isLoading,
    totalPages,
    currentPage,
    
    // Computed
    publishedArticles,
    draftArticles,
    
    // Actions
    fetchArticles,
    fetchArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    publishArticle,
    checkWithAI,
    searchArticles,
    fetchCategories,
    fetchTags,
    fetchMyArticles,
    fetchDrafts,
    init
  }
})
