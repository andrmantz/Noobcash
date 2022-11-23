import React from 'react';
import { Grid, CircularProgress } from '@mui/material';

export default function Spinner() {
  return (
    <Grid container justifyContent="center">
      <CircularProgress sx={{ marginTop: "10px" }}/>
    </Grid>
  );
}