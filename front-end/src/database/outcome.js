const length = Math.round(Math.random()*100);
const data = [];
for (let i=0; i<length; i++) {
    data.push({
        receiver_index: Math.random()*1000,
        receiver_address: "ajhgasjbgasjgbaaskjfgakjsgasdfgsdfhsfdhdgsdhg",
        amount: Math.random()*100, 
        index: i+1, 
    })
}
export const getOutcome = () => {
    return data;
}