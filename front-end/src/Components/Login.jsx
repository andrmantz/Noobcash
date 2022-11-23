import { Alert, Grid, Typography, Divider, Snackbar } from '@mui/material';
import React, { useState, useEffect } from 'react'
import { getAllNodesCall } from '../api';
import Node from './Node';
import Spinner from './Spinner';

const Login = () => {
    const [nodes, setNodes] = useState([]);
    const [node, setNode] = useState(null);
    const [loading, setLoading] = useState(false);
    const [snackContent, setSnackContent] = useState(null);

    const hideSnackbar = () => {
        setSnackContent(null);
    }


    useEffect(() => {
        setLoading(true);
        getAllNodesCall()
        .then(response => {
            console.log({ nodes_resp: response.data });
            setNodes(response.data);
            setLoading(false);
        })
        .catch(err => {
            setLoading(false);
        })
        const port = localStorage.getItem("port") || 5000;
        setNode(`localhost:${port}`);
    }, [])

    const renderSnackbar = () => {
        if (snackContent) {
            const { text, severity } = snackContent;
            return (
                <Snackbar
                    onClose={hideSnackbar}
                    open
                    anchorOrigin={{ vertical: "bottom", horizontal : "center" }}
                    autoHideDuration={6000}
                >
                    <Alert severity={severity} onClose={hideSnackbar}>
                        { text }
                    </Alert>
                </Snackbar>
            )
        }
        return null;
    }


    if (loading) {
        return (
            <Spinner />
        )
    }
    if (!nodes?.length) {
        return (
            <Alert severity="info">
                No active nodes found
            </Alert>
        )
    }
    return (
        <Grid item>
            <Grid container rowSpacing={2}>
                <Grid item xs={12}>
                    <Typography variant="h6">
                        Login as a certain node
                    </Typography>
                </Grid>
                <Divider sx={{ width: 1 }} />
                <Grid item xs={12}>
                    <Grid container spacing={1} justifyContent="center">
                        {nodes.map(({ address, id, label }) => {
                            return (
                                <Grid item key={id} xl={4} md={6} xs={12}>
                                    <Node
                                        address={address}
                                        id={id}
                                        label={label}
                                        selectedNode={node}
                                        setSnackContent={setSnackContent}
                                        setNode={setNode}
                                    />
                                </Grid>
                            )
                        })}
                    </Grid>
                </Grid>
            </Grid>
            { renderSnackbar() }
        </Grid>

    )
}

export default Login;