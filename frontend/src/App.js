import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  CircularProgress,
  Box,
} from '@mui/material';
import axios from 'axios';

function App() {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRankings = async () => {
      try {
        const response = await axios.get('http://localhost:3001/api/rankings');
        setRankings(response.data);
      } catch (err) {
        setError('Failed to fetch rankings');
      } finally {
        setLoading(false);
      }
    };

    fetchRankings();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Fantasy Football Rankings
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell>Player Name</TableCell>
              <TableCell>Position</TableCell>
              <TableCell>Avg Projected Points</TableCell>
              <TableCell>Avg Rank</TableCell>
              <TableCell>Rankings</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rankings.map((ranking, index) => (
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{ranking.name}</TableCell>
                <TableCell>{ranking.pos}</TableCell>
                <TableCell>{ranking.avg_proj_pts}</TableCell>
                <TableCell>{ranking.avg_rank}</TableCell>
                <TableCell>{JSON.stringify(ranking.rankings)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default App;
