import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';

// third-party
import ReactApexChart from 'react-apexcharts';

// chart options
const areaChartOptions = {
  chart: {
    height: 450,
    type: 'area',
    toolbar: {
      show: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 2
  },
  grid: {
    strokeDashArray: 0
  }
};

export default function WeatherAreaChart({ slot }) {
  const theme = useTheme();
  const { primary, secondary } = theme.palette.text;
  const line = theme.palette.divider;

  const [options, setOptions] = useState(areaChartOptions);
  const [series, setSeries] = useState([]);

  useEffect(() => {
    // Configurações do gráfico (eixos e cores)
    setOptions((prevState) => ({
      ...prevState,
      colors: [theme.palette.primary.main, theme.palette.secondary.main],
      xaxis: {
        categories:
          slot === 'month'
            ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            : slot === 'week'
            ? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            : [...Array(24).keys()].map((i) => `${i}:00`),
        labels: {
          style: {
            colors: Array(slot === 'hour' ? 24 : slot === 'week' ? 7 : 12).fill(secondary),
          }
        },
        axisBorder: {
          show: true,
          color: line
        }
      },
      yaxis: [
        {
          labels: {
            style: {
              colors: [theme.palette.primary.main]
            }
          },
          title: {
            text: 'Temperatura (°C)',
            style: {
              color: theme.palette.primary.main
            }
          }
        },
        {
          opposite: true,
          labels: {
            style: {
              colors: [theme.palette.secondary.main]
            }
          },
          title: {
            text: 'Umidade (%)',
            style: {
              color: theme.palette.secondary.main
            }
          }
        }
      ],
      grid: {
        borderColor: line
      }
    }));
  }, [primary, secondary, line, theme, slot]);

  useEffect(() => {
    // Busca dados da rota /data/weather
    const fetchData = async () => {
      try {
        const response = await fetch('http://andromeda.lasdpc.icmc.usp.br:7082/weather/all');
        if (!response.ok) throw new Error('Erro ao buscar dados');
        const data = await response.json();

        // Converte os timestamps para horários legíveis
        const timestamps = data.datetime.map((timestamp) => {
          const date = new Date(timestamp * 1000); // Converte para milissegundos
          return `${date.getHours()}:${date.getMinutes()}`; // Formata como "HH:MM"
        });

        // Atualiza os dados no gráfico
        setSeries([
          {
            name: 'Temperatura',
            data: data.temperatures || [] // Certifique-se que os dados retornados correspondam a esse formato
          },
          {
            name: 'Umidade',
            data: data.humidities || []
          }
        ]);

        // Atualiza as categorias no eixo X com os horários convertidos
        setOptions((prevState) => ({
          ...prevState,
          xaxis: {
            ...prevState.xaxis,
            categories: timestamps,
          }
        }));
      } catch (error) {
        console.error('Erro ao buscar dados do servidor:', error);
      }
    };

    fetchData();
  }, [slot]); // Reexecuta se `slot` mudar

  return <ReactApexChart options={options} series={series} type="area" height={450} />;
}

WeatherAreaChart.propTypes = { slot: PropTypes.string };
