import { Button, Divider, Grid, Paper, Snackbar, Typography } from '@mui/material';
import { blue } from '@mui/material/colors';
import React from 'react'

const Node = ({ address, id, label, selectedNode, setSnackContent, setNode }) => {

    const login = () => {
        localStorage.setItem("port", address.slice(-4));
        localStorage.setItem("id", id);
        setSnackContent({
            text: "Logged in successfully",
            severity: "info",
        });
        setNode(address);
    }

    return (
        <Paper elevation={1} sx={{ padding: 1, bgcolor: (selectedNode===address ? blue[100] : "inherit" )}}>
            <Grid container justifyContent="center" rowSpacing={2}>
                <Grid item xs={12}>
                    <Typography variant="h6" align={"center"}>
                        Node {id}
                    </Typography>
                </Grid>
                <Divider sx={{ width: 1 }} />
                <Grid item xs={12}>
                    <Typography variant="body1" align="center">
                        http://{address}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" fullWidth onClick={login}>
                        Log in
                    </Button>
                </Grid>

            </Grid>
        </Paper>
    )
}

export default Node;