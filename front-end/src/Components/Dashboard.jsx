import { Divider, Grid, Paper, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react'
import { getAllTransactionsCall, getBalanceCall, getIncomesCall, getOutcomesCall } from '../api';
import { getCurrenntBalance } from '../database/balance';
import { getIncome } from '../database/income';
import { getOutcome } from '../database/outcome';
import { getTransactions } from '../database/transactions';
import LineDiagram from './LineDiagram';

const Dashboard = () => {
    const [incomes, setIncomes] = useState([]);
    const [outcomes, setOutcomes] = useState([]);
    const [all, setAll] = useState([]);

    const computeBalanceHistory = (data) => {
        const data_points = [];
        let curr = 0;
        const id = localStorage.getItem("id") || 0;
        const index = 0;
        data.forEach(({ amount, receiver_index, sender_index }) => {
            if (receiver_index==id) {
                curr += amount;
                data_points.push({ amount: curr, index });
            }
            else if (sender_index==id) {
                curr -= amount;
                data_points.push({ amount: curr, index });
            }
        })
        setAll(data_points);
    }

    useEffect(() => {
        getIncomesCall()
        .then(response => {
            console.log(response.data);
            setIncomes(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        getOutcomesCall()
        .then(response => {
            console.log(response.data);
            setOutcomes(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        // setIncomes(getIncome());
        // setOutcomes(getOutcome());
        // setAll(getTransactions());
        getAllTransactionsCall()
        .then(response => {
            console.log(response.data);
            computeBalanceHistory(response.data);
        })
        .catch(err => {
            console.log(err);
        })
    }, [])

    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Typography variant="h5">
                    Welcome, node {localStorage.getItem("id") || 0}
                </Typography>
            </Grid>
            <Divider sx={{ width: 1, margin: 1 }} />
            <Grid item md={6}>
                <StatsPaper title={"Balance History"} data={all} />
            </Grid>
            <Grid item md={6}>
                { CurrentBalance() }
            </Grid>
            <Grid item xs={12} />
            <Grid item md={6}>
                <StatsPaper title={"Incomes History"} data={incomes} />
            </Grid>
            <Grid item md={6}>
                <StatsPaper title={"Outcomes History"} data={outcomes} />
            </Grid>

        </Grid>
    )
}

const StatsPaper = ({ title, data: data_ }) => {
    const [data, setData] = useState([]);
    
    useEffect(() => {
        setData(data_);
    }, [data_])

    const getContent = () => {
        if (data.length) return (
            <LineDiagram data={data} />
        )
        return (
            <Typography variant="body1" align={"center"}>
                No data found
            </Typography>
        )
    }
    
    return (
        <Container
            title={title}
            content={getContent()}
        />
    )
}

const CurrentBalance = () => {
    const [balance, setBalance] = useState(0);

    useEffect(() => {
        getBalanceCall()
        .then(response => {
            console.log(response.data);
            setBalance(response.data);
        })
        // setBalance(getCurrenntBalance());
    }, [])

    return (
        <Container
            title={"Current Balance"}
            content={
                <Typography variant="h6" color="info.main" align={"center"} sx={{ paddingTop: "50px" }}>
                    {balance} NBC
                </Typography>
            }
        />
    )
}

const Container = ({ title, content }) => {
    return (
        <Paper elevation={2} sx={{ height: "300px" }}>
            <Grid container justifyContent={"flex-start"}>
                <Grid item xs={12}>
                    <Typography variant="h6" align={"center"}>
                        { title }
                    </Typography>
                </Grid>
                <Divider sx={{ width: 1, marginTop: 1, marginBottom: 2 }} />
                <Grid item xs={12}>
                    { content }
                </Grid>
            </Grid>
        </Paper>
    )
}

export default Dashboard;