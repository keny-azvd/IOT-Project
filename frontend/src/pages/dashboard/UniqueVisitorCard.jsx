import { useState } from 'react';

// material-ui
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// project import
import MainCard from 'components/MainCard';
import IncomeAreaChart from './IncomeAreaChart';

// ==============================|| DEFAULT - UNIQUE VISITOR ||============================== //

export default function UniqueVisitorCard() {
  const [slot, setSlot] = useState('week');

  return (
    <>
      <Grid container alignItems="center" justifyContent="space-between">
        <Grid item>
          <Typography variant="h5">Clima São Carlos - SP</Typography>
        </Grid>
        <Grid item>
          <Stack direction="row" alignItems="center" spacing={0}>
            
            

          </Stack>
        </Grid>
      </Grid>
      <MainCard content={false} sx={{ mt: 1.5 }}>
        <Box sx={{ pt: 1, pr: 2 }}>
          <IncomeAreaChart slot={slot} />
        </Box>
      </MainCard>
    </>
  );
}
