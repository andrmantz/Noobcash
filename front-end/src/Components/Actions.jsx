import { Send } from "@mui/icons-material";
import { LoadingButton } from "@mui/lab";
import { Alert, Autocomplete, Paper, Divider, Grid, InputAdornment, Snackbar, TextField, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { addTransactionCall, getAllNodesCall, getBalanceCall } from "../api";
import { getNodes } from "../database/nodes";

const Actions = () => {
    const [nodes, setNodes] = useState([]);
    const [amount, setAmount] = useState(0);
    const [value, setValue] = useState("");
    const [inputValue, setInputValue] = useState("");
    const [searchParams, setSearchParams] = useSearchParams();
    const [loading, setLoading] = useState(false);
    const [snackContent, setSnackContent] = useState(null);
    const [balance, setBalance] = useState(0);

    const closeSnack = () => setSnackContent(null); 

    useEffect(() => {
        getAllNodesCall()
        .then(response => {
            console.log(response.data);
            setNodes(
                response.data
                    ?.filter(({ id }) => id!=(localStorage.getItem("id")||0))
                    ?.map(({ address, id, label, public_key }) => ({ address, id, label: `Node ${id}`, public_key }))
                    );
        })
        .catch(err => {
            console.log(err);
        })
        getBalanceCall()
        .then(response => {
            console.log(response.data);
            setBalance(response.data);
        })
        .catch(err => {
            console.log(err);
        })
        // setNodes(getNodes());
    }, [])

    const selectQueryParam = () => {
        if (searchParams.get("to") && nodes?.length) {
            const id_ = searchParams.get("to");
            const goal = nodes.find(({ id, label }) => id==id_);
            console.log({ goal });
            setValue(goal);
            setInputValue(goal);
        }
    }

    useEffect(() => {
        console.log(searchParams.get("to"));
        console.log(nodes);
        selectQueryParam();
    }, [searchParams, nodes])


    const submit = (event) => {
        event.preventDefault();
        console.log({ value: value?.id, amount });
        if (!value) {
            setSnackContent({
                text: "Select a valid node",
                severity: "error",
            });
            return;
        }
        if (!amount || amount <=0) {
            setSnackContent({
                text: "Insert a valid amount",
                severity: "error",
            })
            return;
        }
        if (amount > balance) {
            setSnackContent({
                text: "The amount should be lower than your balance",
                severity: "error",
            })
            return;
        }
        setLoading(true);
        addTransactionCall(value?.id, amount)
        .then(response => {
            console.log(response.data);
            setLoading(false);
            setSnackContent({
                text: "Your transaction was submitted successfully",
                severity: "success",
            })
            setTimeout(() => {
                window.location.reload();
            }, 500)
        })
        .catch(err => {
            console.log(err);
            setLoading(false);
            setSnackContent({
                text: "Sorry, we could not upload your transaction",
                severity: "error",
            })
        })

    }

    const renderSnackMessage = () => {
        if (snackContent) {
            const { text, severity } = snackContent;
            return (
                <Snackbar
                    onClose={closeSnack}
                    open
                    anchorOrigin={{ vertical: "bottom", horizontal : "center" }}
                    autoHideDuration={6000}
                >
                    <Alert severity={severity} onClose={closeSnack}>
                        {text}
                    </Alert>
                </Snackbar>
            )
        }
    }

    return (
        <>
            <Grid container spacing={1}>
                <Grid item xs={12}>
                    <Grid container justifyContent={"space-between"} alignItems="center">
                        <Grid item>
                            <Typography variant="h6">
                                New transaction
                            </Typography>
                        </Grid>
                        <Grid item>
                            <Typography variant="body1" align="center" color="primary">
                                Balance: {balance} NBCs
                            </Typography>
                        </Grid>
                    </Grid>

                </Grid>
                <Divider sx={{ width: 1, marginTop: 1, marginBottom: 2 }} />
                <Grid item xs={12}>
                    <form onSubmit={submit}>
                        <Grid container spacing={2}>
                            <Grid item xl={3} lg={4} md={5} sm={6} xs={6}>
                                <Autocomplete
                                    fullWidth
                                    value={value}
                                    onChange={(event, newValue) => {
                                        setValue(newValue);
                                    }}
                                    inputValue={inputValue}
                                    onInputChange={(event, newInputValue) => {
                                        setInputValue(newInputValue);
                                    }}
                                    id="controllable-states-demo"
                                    options={nodes}
                                    renderInput={(params) => <TextField {...params} label="Receiving node public key" />}
                                />
                            </Grid>
                            <Grid item xl={3} lg={4} md={5} sm={6} xs={6}>
                                <TextField
                                    fullWidth
                                    id="outlined-basic"
                                    label="Amount (NBC)"
                                    variant="outlined"
                                    value={amount}
                                    InputProps={{
                                        type: "number",
                                    }}
                                    onChange={(e) => setAmount(e.target.value)}
                                />
                            </Grid>
                            <Grid item xs={12} />
                            <Grid item>
                                <Grid container justifyContent={"flex-start"}>
                                    <LoadingButton loading={loading} type="submit" variant="contained" endIcon={<Send />}>
                                        Send
                                    </LoadingButton>
                                </Grid>
                            </Grid>
                        </Grid>
                    </form>
                </Grid>
            </Grid>
            { renderSnackMessage() }
        </>
    )
}

export default Actions;