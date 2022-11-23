const length = Math.round(Math.random()*20);
const data = [];
for (let i=0; i<length; i++) {
    const id = Math.round(Math.random()*1000);
    data.push({
        id,
        label: `asl${Math.round(Math.random()*1000)}fj${Math.round(Math.random()*1000)}nas${Math.round(Math.random()*1000)}ljfa${Math.round(Math.random()*1000)}osf`,
    })
}
export const getNodes = () => {
    return data;
}