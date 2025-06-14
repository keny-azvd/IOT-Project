import PropTypes from 'prop-types';

// material-ui
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';

// project import
import AuthFooter from 'components/cards/AuthFooter';
import Logo from 'components/logo';
import AuthCard from './AuthCard';

// assets
import AuthBackground from 'assets/images/auth/AuthBackground';

// ==============================|| AUTHENTICATION - WRAPPER ||============================== //

export default function AuthWrapper({ children }) {
  return (
    <Box sx={{ minHeight: '100vh' }}>
      
    </Box>
  );
}

AuthWrapper.propTypes = { children: PropTypes.node };
