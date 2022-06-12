<template>
  <div class="info-container">
    <q-card
      flat
      bordered
      class="rounded info-temperature text-secondary no-margin card-info-bg no-shadow"
    >
      <!-- Temperature -->
      <q-card-section>
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-subtitle1 text-secondary">TEMPERATURE</div>
            <div class="text-h3 text-info">{{ currentTemperature }}</div>
            <div class="text-subtitle1 text-secondary">TIME</div>
            <div class="text-h5 text-info">{{ currentTime }}</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <q-card
      flat
      bordered
      class="rounded info-targetTemperature text-secondary no-margin card-info-bg no-shadow"
    >
      <!-- Target Temperature -->
      <q-card-section>
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-subtitle1 text-secondary">TARGET TEMPERATURE</div>
            <div class="text-h3 text-info">{{ targetTemperature }}</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <q-card
      flat
      bordered
      class="rounded info-pid text-secondary no-margin card-info-bg no-shadow"
    >
      <!-- Current Settings -->
      <q-card-section class="q-pb-xs">
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-subtitle1 text-secondary">CONFIGURATION</div>
            <div class="pid-container">
              <div class="text-h5 text-weight-bold pid-item text-info">
                P:<span class="text-h5">{{ P }}</span>
              </div>
              <div class="text-h5 text-weight-bold pid-item text-info">
                I:<span class="text-h5">{{ I }}</span>
              </div>
              <div class="text-h5 text-weight-bold pid-item text-info">
                D:<span class="text-h5">{{ D }}</span>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>

      <!-- Settings -->
      <q-card-actions class="justify-center q-pt-xs">
        <q-btn
          color="positive"
          text-color="warning"
          size="22px"
          icon="settings"
          label="Settings"
          class="full-width rounded"
          @click="
            updateForm();
            settings = true;
          "
        />
      </q-card-actions>
    </q-card>

    <q-dialog
      v-model="settings"
      persistent
      transition-show="flip-down"
      transition-hide="flip-up"
    >
      <q-card class="rounded">
        <q-card-section
          class="row items-center q-pb-none card-settings-bg bg-warning text-secondary"
        >
          <div class="text-h5 text-secondary">PID Settings</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
          <q-btn
            icon="done"
            flat
            round
            dense
            v-close-popup
            @click="passEvent()"
          />
        </q-card-section>

        <q-card-section class="bg-warning">
          <div class="settings-container">
            <div class="settings-item">
              <q-input
                rounded
                input-class="card-settings-text"
                standout="bg-dark"
                bg-color="--negative"
                v-model="form_P"
                label="P"
                label-color="info"
                :dense="dense"
              >
              </q-input>
            </div>
            <div class="settings-item">
              <q-input
                rounded
                input-class="card-settings-text"
                standout="bg-dark"
                bg-color="--negative"
                v-model="form_I"
                label="I"
                label-color="info"
                :dense="dense"
              >
              </q-input>
            </div>
            <div class="settings-item">
              <q-input
                rounded
                input-class="card-settings-text"
                standout="bg-dark"
                bg-color="--negative"
                v-model="form_D"
                label="D"
                label-color="info"
                :dense="dense"
              >
              </q-input>
            </div>
            <div class="settings-item2">
              <q-input
                rounded
                input-class="card-settings-text"
                standout="bg-dark"
                bg-color="--negative"
                v-model="form_targetTemperature"
                label="Target Temperature"
                label-color="info"
                :dense="dense"
              >
              </q-input>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<style></style>

<script>
export default {
  name: "Info",
  props: [
    "P",
    "I",
    "D",
    "targetTemperature",
    "currentTemperature",
    "currentTime",
    "pidRecieved",
  ],

  data: function () {
    return {
      displayTemperature: 0,
      form_P: this.P,
      form_I: this.I,
      form_D: this.D,
      form_targetTemperature: this.targetTemperature,
    };
  },
  methods: {
    passEvent() {
      var data = {
        P: this.form_P,
        I: this.form_I,
        D: this.form_D,
        targetTemperature: this.form_targetTemperature,
      };
      this.$emit("setPID", data);
      setTimeout(() => this.showNotification(), 100);
    },
    updateForm() {
      this.form_P = this.P;
      this.form_I = this.I;
      this.form_D = this.D;
      this.form_targetTemperature = this.targetTemperature;
    },
    showNotification() {
      if (this.pidRecieved == true) {
        this.$q.notify({
          icon: null,
          color: "green",
          position: "top",
          message: "PID settings updated successfully!",
          timeout: 3000,
        });
      }
    },
  },
};
</script>
