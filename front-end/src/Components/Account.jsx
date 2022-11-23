import { Alert, Divider, Grid, Paper, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { getProfileInfoCall } from "../api";
import { getProfileInfo } from "../database/profile";

const Account = () => {
    const [data, setData] = useState({});

    useEffect(() => {
        getProfileInfoCall()
        .then(response => {
            console.log(response.data);
            setData(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        // setData(getProfileInfo());
    }, [])

    const { public_key, id } = data || {};

    if (!public_key) {
        return (
            <Alert severity="info">
                Sorry, we could not obtain your info
            </Alert>
        )
    }
    return (
        <Grid container spacing={3}>
            <Grid item lg={3} md={4} sm={6} xs={6} minHeight={100}>
                <Paper sx={{ height: 1, padding: 1 }}>
                    <Typography variant="h6">
                        My id
                    </Typography>
                    <Divider sx={{ marginTop: 1, marginBottom: 2 }} />
                    <Typography variant="body1" fontWeight={"bold"}>
                        { id }
                    </Typography>
                </Paper>
            </Grid>
            <Grid item xs={12}>
                <Paper sx={{ height: 1, padding: 1 }}>
                    <Typography variant="h6">
                        My public key
                    </Typography>
                    <Divider sx={{ marginTop: 1, marginBottom: 2 }} />
                    <Typography sx={{ height: 1, wordBreak: "break-all" }} variant="body1" fontWeight={"bold"}>
                        { public_key }
                    </Typography>
                </Paper>
            </Grid>

        </Grid>
    )
}

export default Account;