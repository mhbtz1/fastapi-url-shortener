import { createRoot } from 'react-dom/client'
import { App } from './App'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner';

const queryClient = new QueryClient()

const root = document.getElementById('root')!

createRoot(root).render(
<QueryClientProvider client={queryClient}> 
    <Toaster richColors/>
     <App/> 
</QueryClientProvider>)