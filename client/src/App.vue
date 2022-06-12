<template>
  <q-layout view="hHh lpR fFf" :class="{ bgimage: background, bgcolour: !background}">
    <q-page-container>
      <!-- <Graph /> -->
      <q-page>
        <div class="box">
          <div class="row text-center">
            <div class="col">
              <h1 class="text-center fontHeader text-primary">
                {{ settings.VUE_TITLE }}
              </h1>
            </div>
          </div>

          <div class="row content justify-center">
            <!-- Graph -->
            <div
              ref="graph"
              class="graph col-xs-12 col-sm-12 col-md-9 col-lg-6 col-xl-6 q-pa-sm"
            >
              <Graph
                v-bind:dataArray="dataArray"
                v-bind:chartHeight="chartHeight"
                v-bind:targetTemperature="targetTemperature"
                v-bind:settings="settings"
              />
            </div>

            <!-- Info -->
            <div
              class="info col-xs-12 col-sm-12 col-md-3 col-lg-2 col-xl-3 q-pa-sm"
            >
              <Info
                v-bind:P="P"
                v-bind:I="I"
                v-bind:D="D"
                v-bind:targetTemperature="targetTemperature"
                v-bind:currentTemperature="currentTemperature"
                v-bind:currentTime="currentTime"
                v-bind:pidRecieved="pidRecieved"
                @setPID="setPID($event)"
              />
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
// imports setup
import Graph from "./components/Graph.vue";
import Info from "./components/Info.vue";
import "./styles/customCSS.css";
import io from "socket.io-client";

// Socket setup
var socket = io();

export default {
  inject: ["settings"],
  components: {
    Graph,
    Info,
  },
  data() {
    return {
      P: "",
      I: "",
      D: "",
      targetTemperature: "",
      currentTemperature: "",
      currentTime: "",
      dataArray: [],

      vueSocketEndpoint: "",

      chartHeight: null,
      pidRecieved: false,

      background: true,
    };
  },
  created() {
    this.setColours();
    this.getTemperature();
    this.getPID();
    document.title = this.settings.VUE_TITLE;
  },
  beforeMount() {
    this.getPID();
  },
  mounted() {
    this.askForTemperature();
    this.askForPID();
    this.$nextTick(function () {
      window.addEventListener("resize", this.updateChartHeight);
      this.updateChartHeight();
    });
  },
  methods: {
    getTemperature() {
      socket.on("recieve_temperature", (fetchedData) => {
        this.dataArray = fetchedData;
        this.currentTemperature = fetchedData.at(-1).y.toFixed(2);

        let currentTimeFormatted = new Date(fetchedData.at(-1).x);
        var hours = currentTimeFormatted.getHours();
        var minutes = currentTimeFormatted.getMinutes();
        var seconds = currentTimeFormatted.getSeconds();
        var ampm = hours >= 12 ? "pm" : "am";
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        var strTime = hours + ":" + minutes + ":" + seconds + " " + ampm;
        this.currentTime = strTime;
      });
    },
    getPID() {
      socket.on("give_PID", (fetchedData) => {
        this.P = fetchedData["PID"]["P"];
        this.I = fetchedData["PID"]["I"];
        this.D = fetchedData["PID"]["D"];
        this.targetTemperature = fetchedData["TargetTemperature"];

        this.pidRecieved = true;
        setTimeout(() => (this.pidRecieved = false), 3000);
      });
    },
    askForTemperature: function () {
      setInterval(function () {
        socket.emit("send_temperature");
      }, 500);
    },
    askForPID: function () {
      socket.emit("get_PID");
    },
    setPID: function (data) {
      socket.emit("send_PID", data);
    },
    updateChartHeight() {
      this.chartHeight = this.$refs.graph.clientHeight;
    },
    setColours() {
      let root = document.documentElement;
      if(this.settings.BACKGROUND_IMAGE == true){
        this.background = true;
      }else{
        this.background = false;
      }

      root.style.setProperty("--primary", this.settings.VUE_COLOUR.primary);
      root.style.setProperty("--secondary", this.settings.VUE_COLOUR.secondary);
      root.style.setProperty("--accent", this.settings.VUE_COLOUR.accent);
      root.style.setProperty("--dark", this.settings.VUE_COLOUR.dark);
      root.style.setProperty("--positive", this.settings.VUE_COLOUR.positive);
      root.style.setProperty("--negative", this.settings.VUE_COLOUR.negative);
      
      root.style.setProperty("--info", this.settings.VUE_COLOUR.info);
      root.style.setProperty("--warning", this.settings.VUE_COLOUR.warning);
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 12px;
}
.container {
  display: flex;
  flex-direction: column;
  padding: 0 24px;
}
.container__item {
  padding: 12px;
  width: 100%;
  margin-top: 24px;
}
</style>
