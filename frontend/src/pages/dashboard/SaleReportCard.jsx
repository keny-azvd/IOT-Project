import { useState } from 'react';

// material-ui
import Grid from '@mui/material/Grid';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

// project import
import SalesChart from './SalesChart';

// sales report status
const status = [
  {
    value: 'today',
    label: 'Today'
  },
  {
    value: 'month',
    label: 'This Month'
  },
  {
    value: 'year',
    label: 'This Year'
  }
];

// ==============================|| DEFAULT - SALES REPORT ||============================== //

export default function SaleReportCard() {
  const [value, setValue] = useState('today');

  return (
    <>
      <Grid container alignItems="center" justifyContent="space-between">
    
      
      </Grid>
      <SalesChart />
    </>
  );
}
