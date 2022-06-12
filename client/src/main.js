import { createApp } from "vue";
import App from "./App.vue";
import { Quasar, Notify } from "quasar";
import quasarUserOptions from "./quasar-user-options";

// import axios from "axios";

async function getSettings() {
  // let res = await axios.get("/settings");
  // return await res.data;
  let json = {
    VUE_TITLE: "Espresso Machine",
    BACKGROUND_IMAGE: false,
    VUE_COLOUR: {
      primary: "#0da54e", // page title
      secondary: "#0da54e", // card heading
      accent: "#f48221", //graph line
      dark: "#f2f2f2", //graph bg
      positive: "#0da54e", //settings fill
      negative: "#d2d6d9", //BACKGROUND colour
      info: "#0da54e", // card text / graph outline
      warning: "#f2f2f2", // card bg
    },
    FLASK_IP: "0.0.0.0",
    FLASK_PORT: 5000,
  };
  return json;
}

getSettings().then((res) => {
  createApp(App)
    .use(
      Quasar,
      {
        plugins: {
          Notify,
        },
        config: {
          notify: {
            /* look at QuasarConfOptions from the API card */
          },
          brand: {
            primary: res.VUE_COLOUR.primary,
            secondary: res.VUE_COLOUR.secondary,
            accent: res.VUE_COLOUR.accent,
            dark: res.VUE_COLOUR.dark,
            positive: res.VUE_COLOUR.positive,
            negative: res.VUE_COLOUR.negative,
            info: res.VUE_COLOUR.info,
            warning: res.VUE_COLOUR.warning,
          },
        },
      },
      quasarUserOptions
    )
    .provide("settings", res)
    .mount("#app");
});
