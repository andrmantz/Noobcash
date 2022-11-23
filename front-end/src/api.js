import axios from "axios";

const getBaseUrl = () => {
    const port = localStorage.getItem("port") || 5000;
    return `http://localhost:${port}`;
}

export const getIncomesCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/incomes`;
    return axios.get(requestUrl);
}

export const getOutcomesCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/outcomes`;
    return axios.get(requestUrl);
}

export const getAllTransactionsCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/transactions`;
    return axios.get(requestUrl);
}

export const addTransactionCall = (id, amount) => {
    const base = getBaseUrl();
    const requestUrl = `${base}/create_transaction`;
    const body = {
        id,
        amount,
    };
    console.log(body);
    return axios.post(requestUrl, body);
}

export const getProfileInfoCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/profile`;
    return axios.get(requestUrl);
}

export const getAllNodesCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/nodes`;
    return axios.get(requestUrl);
}

export const getBalanceCall = () => {
    const base = getBaseUrl();
    const requestUrl = `${base}/balance`;
    return axios.get(requestUrl);
}