<template>
  <div class="space-y-12">
    <!-- Hero Section -->
    <section class="text-center py-16 bg-gradient-to-br from-primary-50 to-blue-50 rounded-2xl">
      <div class="max-w-4xl mx-auto px-4">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Bienvenue sur
          <span class="text-primary-600">MiniBlog</span>
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Un blog moderne et épuré avec vérification IA du contenu. 
          Partagez vos idées et laissez l'intelligence artificielle vous aider à créer du contenu de qualité.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link 
            to="/articles" 
            class="btn btn-primary text-lg px-8 py-3"
          >
            Découvrir les articles
          </router-link>
          <router-link 
            v-if="!authStore.isAuthenticated"
            to="/register" 
            class="btn btn-outline text-lg px-8 py-3"
          >
            Commencer à écrire
          </router-link>
        </div>
      </div>
    </section>
    
    <!-- Articles récents -->
    <section>
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-3xl font-bold text-gray-900">Articles récents</h2>
        <router-link 
          to="/articles" 
          class="text-primary-600 hover:text-primary-700 font-medium"
        >
          Voir tous les articles →
        </router-link>
      </div>
      
      <div v-if="articlesStore.isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600">Chargement des articles...</p>
      </div>
      
      <div v-else-if="recentArticles.length === 0" class="text-center py-12">
        <p class="text-gray-600">Aucun article publié pour le moment.</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <article 
          v-for="article in recentArticles" 
          :key="article.id"
          class="card hover:shadow-lg transition-shadow duration-300"
        >
          <!-- Image de l'article -->
          <div v-if="article.featured_image" class="mb-4">
            <img 
              :src="article.featured_image" 
              :alt="article.title"
              class="w-full h-48 object-cover rounded-lg"
            />
          </div>
          
          <!-- Contenu -->
          <div class="space-y-3">
            <!-- Catégorie et tags -->
            <div class="flex items-center gap-2 flex-wrap">
              <span v-if="article.category" class="badge badge-primary">
                {{ article.category.name }}
              </span>
              <span 
                v-for="tag in article.tags.slice(0, 2)" 
                :key="tag.id"
                class="badge badge-secondary"
              >
                {{ tag.name }}
              </span>
            </div>
            
            <!-- Titre -->
            <h3 class="text-xl font-bold text-gray-900 line-clamp-2">
              <router-link 
                :to="{ name: 'ArticleDetail', params: { slug: article.slug } }"
                class="hover:text-primary-600 transition-colors"
              >
                {{ article.title }}
              </router-link>
            </h3>
            
            <!-- Extrait -->
            <p v-if="article.excerpt" class="text-gray-600 line-clamp-3">
              {{ article.excerpt }}
            </p>
            
            <!-- Métadonnées -->
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div class="flex items-center space-x-4">
                <span>{{ formatDate(article.published_at || article.created_at) }}</span>
                <span>{{ article.reading_time }} min de lecture</span>
              </div>
              
              <!-- Score IA si disponible -->
              <div v-if="article.ai_checked && article.ai_score" class="flex items-center space-x-1">
                <span class="text-xs">IA:</span>
                <span 
                  :class="getScoreColor(article.ai_score)"
                  class="font-medium"
                >
                  {{ article.ai_score }}/10
                </span>
              </div>
            </div>
            
            <!-- Auteur -->
            <div class="flex items-center space-x-2 pt-2 border-t border-gray-100">
              <div class="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center">
                <span class="text-primary-600 text-xs font-medium">
                  {{ getAuthorInitials(article.author) }}
                </span>
              </div>
              <span class="text-sm text-gray-600">
                {{ article.author.first_name }} {{ article.author.last_name }}
              </span>
            </div>
          </div>
        </article>
      </div>
    </section>
    
    <!-- Statistiques -->
    <section class="bg-white rounded-2xl p-8 border border-gray-200">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">MiniBlog en chiffres</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600 mb-2">
            {{ totalArticles }}
          </div>
          <p class="text-gray-600">Articles publiés</p>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600 mb-2">
            {{ totalCategories }}
          </div>
          <p class="text-gray-600">Catégories</p>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600 mb-2">
            {{ articlesWithAI }}
          </div>
          <p class="text-gray-600">Articles vérifiés par l'IA</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Home',
  setup() {
    const articlesStore = useArticlesStore()
    const authStore = useAuthStore()
    
    // Computed
    const recentArticles = computed(() => 
      articlesStore.publishedArticles.slice(0, 6)
    )
    
    const totalArticles = computed(() => 
      articlesStore.publishedArticles.length
    )
    
    const totalCategories = computed(() => 
      articlesStore.categories.length
    )
    
    const articlesWithAI = computed(() => 
      articlesStore.publishedArticles.filter(article => article.ai_checked).length
    )
    
    // Methods
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const getScoreColor = (score) => {
      if (score >= 8) return 'text-green-600'
      if (score >= 6) return 'text-yellow-600'
      return 'text-red-600'
    }
    
    const getAuthorInitials = (author) => {
      if (!author) return ''
      const { first_name, last_name, username } = author
      if (first_name && last_name) {
        return `${first_name[0]}${last_name[0]}`.toUpperCase()
      }
      return username[0].toUpperCase()
    }
    
    // Lifecycle
    onMounted(async () => {
      await Promise.all([
        articlesStore.fetchArticles(),
        articlesStore.init()
      ])
    })
    
    return {
      articlesStore,
      authStore,
      recentArticles,
      totalArticles,
      totalCategories,
      articlesWithAI,
      formatDate,
      getScoreColor,
      getAuthorInitials
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
