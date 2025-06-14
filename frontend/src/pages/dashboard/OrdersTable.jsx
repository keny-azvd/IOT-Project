import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { Line } from 'react-chartjs-2'; // Importando o gráfico
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Registrando os componentes do Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Funções de ordenação da tabela
function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) {
      return order;
    }
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

// Cabeçalho da tabela com as novas colunas
const headCells = [
  { id: 'tracking_no', align: 'left', disablePadding: false, label: 'ID' },
  { id: 'name', align: 'left', disablePadding: true, label: 'Dispositivo' },
  { id: 'temperature', align: 'center', disablePadding: false, label: 'Temperatura' },
  { id: 'humidity', align: 'center', disablePadding: false, label: 'Umidade' },
  { id: 'atuador', align: 'center', disablePadding: false, label: 'Atuador' },
  { id: 'details', align: 'center', disablePadding: false, label: 'Detalhes' }
];

function OrderTableHead({ order, orderBy }) {
  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.align}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            {headCell.label}
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

export default function OrderTable() {
  const [rows, setRows] = useState([]);
  const [open, setOpen] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });
  const order = 'asc';
  const orderBy = '_id';

  // Função para atualizar o status do atuador
  const toggleActuatorStatus = async (name, currentStatus) => {
    try {
      const response = await fetch(`http://andromeda.lasdpc.icmc.usp.br:7082/command/${name}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ actuator_status: !currentStatus })
      });

      if (!response.ok) {
        throw new Error('Failed to update actuator status');
      }

      const updatedRows = rows.map((row) =>
        row.name === name ? { ...row, actuator_status: !currentStatus } : row
      );
      setRows(updatedRows);
    } catch (error) {
      console.error('Error updating actuator status:', error);
    }
  };

  // Função para buscar dados do dispositivo
  const fetchDeviceData = async (name) => {
    try {
      const response = await fetch(`http://andromeda.lasdpc.icmc.usp.br:7082/mcu/${name}/data_weather`);
      if (!response.ok) {
        throw new Error(`Failed to fetch data for ${name}`);
      }
      const data = await response.json();
      return data; // Supondo que o backend retorne { temperature, humidity }
    } catch (error) {
      console.error('Error fetching device data:', error);
      return { temperature: '-', humidity: '-' }; // Valor default em caso de erro
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://andromeda.lasdpc.icmc.usp.br:7082/mcu/all');
        if (!response.ok) {
          throw new Error('Failed to fetch devices');
        }
        const data = await response.json();
  
        const updatedRows = await Promise.all(data.map(async (device) => {
          const weatherData = await fetchDeviceData(device.name);  // Buscando temperatura e umidade
          return { ...device, 
            tracking_no: device._id?.$oid,
            temperature: weatherData.temperature, 
            humidity: weatherData.humidity };
        }));
  
        setRows(updatedRows);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();
  }, []);
  
  // Função que é chamada quando o modal é aberto para carregar os dados específicos do gráfico
  useEffect(() => {
    if (selectedDevice) {
      const loadChartData = async () => {
        const data = await fetchDeviceChartData(selectedDevice.name); // Usando o nome do dispositivo
        
        setChartData({
          labels: data.timestamp.map(ts => new Date(ts).toLocaleTimeString()), // Convertendo os timestamps para hora legível
          datasets: [
    {
      label: 'Temperatura (°C)',
      data: data.temperature,
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      fill: true,
      tension: 0.4,  // Suaviza a linha da temperatura
      pointRadius: 0,

      pointHoverRadius: 5,  // Tamanho do ponto ao passar o mouse
      yAxisID: 'y',
    },
    {
      label: 'Umidade (%)',
      data: data.humidity,
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      fill: true,
      tension: 0.4,  // Suaviza a linha da umidade
      yAxisID: 'y1',
      pointRadius: 0,
      pointHoverRadius: 5,  // Tamanho do ponto ao passar o mouse

    },
  ],
        });
      };
  
      loadChartData();
    }
  }, [selectedDevice]);  // Quando selectedDevice mudar, chama a função para carregar os dados do gráfico

  // Função para abrir o modal com as informações do dispositivo
  const handleOpen = (device) => {
    setSelectedDevice(device);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedDevice(null);
  };

  const fetchDeviceChartData = async (deviceName) => {
    try {
      const response = await fetch(`http://andromeda.lasdpc.icmc.usp.br:7082/mcu/${deviceName}/list_data_weather`);
      if (!response.ok) {
        throw new Error(`Failed to fetch weather data for device ${deviceName}`);
      }
      const data = await response.json(); // Supondo que o backend retorne { temperature: [], humidity: [], timestamp: [] }
      return data;
    } catch (error) {
      console.error('Error fetching chart data:', error);
      return { temperature: [], humidity: [], timestamp: [] }; // Valores padrão em caso de erro
    }
  };
  

  const chartOptions = {
    responsive: true,
    scales: {
      x: {
        title: {
          display: true,
          text: 'Horário',
        },
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10, // Limita o número de rótulos para evitar poluição visual
        },
      },
      y: {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: 'Temperatura (°C)',
        },
      },
      y1: {
        type: 'linear',
        position: 'right',
        title: {
          display: true,
          text: 'Umidade (%)',
        },
      },
    },
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
      </Typography>
      <TableContainer style={{ width: '100%'}}>
        <Table style={{ width: '100%' }}>
          <OrderTableHead order={order} orderBy={orderBy} />
          <TableBody>
            {stableSort(rows, getComparator(order, orderBy)).map((row) => (
              <TableRow key={row.name}>
                <TableCell align="left">{row.tracking_no}</TableCell>
                <TableCell align="left">{row.name}</TableCell>
                <TableCell align="center">
                  {row.temperature !== '-' ? `${row.temperature} °C` : '-'}
                </TableCell>                
                <TableCell align="center">
                  {row.humidity !== '-' ? `${row.humidity} %` : '-'}
                </TableCell>                
                <TableCell align="center">
                  <Button onClick={() => toggleActuatorStatus(row.name, row.actuator_status)}>
                    {row.actuator_status ? 'Desligar Atuador' : 'Ligar Atuador'}
                  </Button>
                </TableCell>
                <TableCell align="center">
                  <Button onClick={() => handleOpen(row)}>Ver Detalhes</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
  
      <Dialog open={open} onClose={handleClose} fullWidth maxWidth="md">
        <DialogTitle>{selectedDevice?.name}</DialogTitle>
        <DialogContent>
          <Line data={chartData} options={chartOptions} />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

OrderTable.propTypes = {
  rows: PropTypes.array,
};
