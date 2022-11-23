const length = Math.round(Math.random()*100);
const data = [];
for (let i=0; i<length; i++) {
    data.push({
        sender_index: Math.random()*1000,
        sender_address: "ajhgasjbgasjgbaaskjfgakjsgasdfgsdfhsfdhdgsdhg",
        amount: Math.random()*100, 
        index: i+1,
    })
}
export const getTransactions = () => {
    return data;
}