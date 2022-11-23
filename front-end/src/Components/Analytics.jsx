import { Info } from '@mui/icons-material';
import { Grid, Paper, Typography, Box, Tab, Tabs, Tooltip, Button } from '@mui/material';
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { getIncomesCall, getOutcomesCall } from '../api';
import { getIncome } from '../database/income';
import { getOutcome } from '../database/outcome';
import TabPanel from "./TabPanel";

function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
}

const Transaction = ({ receiver_index, receiver_address, sender_index, sender_address, amount, receiving=false, index }) => {
    // const navigate = useNavigate();
    let node = Math.round(receiver_index);
    let address = receiver_address;
    let main = `To node ${node}`;
    let msg= "Send some NBC again";
    if (receiving) {
        address = sender_address;
        node = Math.round(sender_index)
        main = `From node ${node}`;
        msg = "Send some NBC back";
    }
    if (node===-1) {
        main = "Genesis block";
    }
    const sendTo = () => {
        // navigate(`/actions?to=${address}`);
        window.location.href = (`/actions?to=${node}`);
    }
    return (
        <Grid item lg={3} md={4} sm={6} xs={6} key={index} height={"auto"}>
            <Paper elevation={3} sx={{ height: "100%", width: "100%" }}>
                <Grid container height={1} padding={2} alignContent="space-between">
                    <Grid item xs={12}>
                        <Grid item xs={12}>
                            <Typography variant="body1" fontWeight={"bold"}>
                                {Math.round(amount, 2)} NBC
                            </Typography>
                        </Grid>
                        <Grid item xs={12}>
                            <Grid container spacing={1}>
                                <Grid item>
                                <Typography variant="body2">
                                    { main }
                                </Typography>
                                </Grid>
                                {node!==-1 &&
                                    <Grid item>
                                        <Tooltip arrow title={`public key: ${address}`}>
                                            <Info fontSize='small' />
                                        </Tooltip>
                                    </Grid>
                                }
                            </Grid>
                        </Grid>
                    </Grid>
                    {node!==-1 &&
                        <Grid item xs={12}>
                            <Button onClick={()=>sendTo(address)} size="small" variant="contained">
                                { msg }
                            </Button>
                        </Grid>                    
                    }
                </Grid>
            </Paper>
        </Grid>
    )
}

const Analytics = () => {
    const [incomes, setIncomes] = useState([]);
    const [outcomes, setOutcomes] = useState([]);
    const [value, setValue] = React.useState(0);

    useEffect(() => {
        getIncomesCall()
        .then(response => {
            console.log(response.data);
            setIncomes(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        // setIncomes(getIncome());
        getOutcomesCall()
        .then(response => {
            console.log(response.data);
            setOutcomes(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        // setOutcomes(getOutcome());
    }, [])

    const handleChange = (event, newValue) => {
      setValue(newValue);
    };
  
    return (
      <Box sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs centered value={value} onChange={handleChange} aria-label="basic tabs example">
            <Tab label="Incomes" {...a11yProps(0)} />
            <Tab label="Outcomes" {...a11yProps(1)} />
          </Tabs>
        </Box>
        <TabPanel value={value} index={0}>
            { ComesKind({ data: incomes, title: "Incomes History", receiving: true })}
        </TabPanel>
        <TabPanel value={value} index={1}>
            { ComesKind({ data: outcomes, title: "Incomes History", receiving: false })}
        </TabPanel>
      </Box>
    );
}

const ComesKind = ({ data, receiving }) => {

    return (
        <Grid item xs={12}>
            <Grid container padding={2} spacing={1}>
                {data.map((datum, index) => {
                    return (
                        Transaction({ ...datum, receiving, index })
                    )})
                }
            </Grid>
        </Grid>
    )
}

export default Analytics;