import { createBrowserRouter } from 'react-router-dom';

// project import
import MainRoutes from './MainRoutes';
import LoginRoutes from './LoginRoutes';

// ==============================|| ROUTING RENDER ||============================== //

const router = createBrowserRouter([MainRoutes, LoginRoutes], {   basename: import.meta.env.VITE_APP_BASE_NAME || '/free', // Define /free como base para todas as rotas
 });

export default router;
