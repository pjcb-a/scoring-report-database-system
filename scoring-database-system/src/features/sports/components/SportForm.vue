<script setup>
import {

  computed,

  onMounted,

  ref

} from 'vue'

import {

  useSportStore

} from '../store/sportStore'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  getScoringTypes

} from '../services/sportService'


/*
------------------------------------------------------------------------------
EMITS
------------------------------------------------------------------------------
*/

const emit = defineEmits([

  'success',

  'close'
])

/*
------------------------------------------------------------------------------
STORES
------------------------------------------------------------------------------
*/

const sportStore =
  useSportStore()

const eventContextStore =
  useEventContextStore()

/*
------------------------------------------------------------------------------
STATE
------------------------------------------------------------------------------
*/

const sportName = ref('')

const scoringTypeId = ref('')

const saving = ref(false)

const scoringTypes = ref([])

const loadingScoringTypes = ref(false)

/*
------------------------------------------------------------------------------
COMPUTED
------------------------------------------------------------------------------
*/

const currentEvent =
  computed(() => {

    return eventContextStore
      .currentEvent
  })

const currentEventId =
  computed(() => {

    return eventContextStore
      .currentEventId
  })

/*
------------------------------------------------------------------------------
FETCH SCORING TYPES
------------------------------------------------------------------------------
*/

const fetchScoringTypes =
  async () => {

    loadingScoringTypes.value = true

    try {

      const response =
        await getScoringTypes()

      /*
      ------------------------------------------------------------------------
      TRANSFORM DATA TO MATCH SELECT OPTIONS FORMAT
      ------------------------------------------------------------------------
      */

      scoringTypes.value =
        response.data.map(type => ({

          value: type.scoring_type_id,

          label: type.scoring_name
        }))

    } catch (err) {

      console.error(
        'Failed to fetch scoring types:',
        err
      )

      scoringTypes.value = []

    } finally {

      loadingScoringTypes.value = false
    }
  }

/*
------------------------------------------------------------------------------
LIFECYCLE
------------------------------------------------------------------------------
*/

onMounted(() => {

  fetchScoringTypes()
})

/*
------------------------------------------------------------------------------
SUBMIT SPORT
------------------------------------------------------------------------------
*/

const submitSport =
  async () => {

    /*
    --------------------------------------------------------------------------
    VALIDATE EVENT
    --------------------------------------------------------------------------
    */

    if (!currentEventId.value) {

      return
    }

    /*
    --------------------------------------------------------------------------
    VALIDATE FORM
    --------------------------------------------------------------------------
    */

    if (

      !sportName.value ||

      !scoringTypeId.value
    ) {

      return
    }

    saving.value = true

    try {

      /*
      ------------------------------------------------------------------------
      CREATE EVENT SPORT
      ------------------------------------------------------------------------
      */

      await sportStore.addSport({

        sport_name:
          sportName.value,

        scoring_type_id:
          scoringTypeId.value
      })

      /*
      ------------------------------------------------------------------------
      RESET FORM
      ------------------------------------------------------------------------
      */

      sportName.value = ''

      scoringTypeId.value = ''

      /*
      ------------------------------------------------------------------------
      SUCCESS + CLOSE
      ------------------------------------------------------------------------
      */

      emit('success')

      emit('close')

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }
</script>

<template>

  <div class="modal-overlay">

    <div class="sport-form-modal card-base">

      <!-- HEADER -->

      <div class="form-header">

        <div>

          <h2>
            Add Sport
          </h2>

          <p>
            Create a sport unique to this event.
          </p>

        </div>

        <button
          class="close-btn"
          @click="emit('close')"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>

      </div>

      <!-- ACTIVE EVENT -->

      <div
        v-if="currentEvent"
        class="active-event-banner"
      >

        <i class="fa-solid fa-calendar-days"></i>

        <span>
          {{ currentEvent.event_name }}
        </span>

      </div>

      <!-- FORM -->

      <div class="form-body">

        <!-- SPORT NAME -->

        <div class="form-group">

          <label for="sport-name">
            Sport Name
          </label>

          <input

            id="sport-name"

            v-model="sportName"

            type="text"

            class="form-input"

            placeholder="Enter sport name"
          />

        </div>

        <!-- SCORING TYPE -->

        <div class="form-group">

          <label for="scoring-type">
            Scoring Type
          </label>

          <select

            id="scoring-type"

            v-model="scoringTypeId"

            class="form-input"

            :disabled="loadingScoringTypes"
          >

            <option value="">
              {{ loadingScoringTypes ? 'Loading...' : 'Select Scoring Type' }}
            </option>

            <option

              v-for="type in scoringTypes"

              :key="type.value"

              :value="type.value"
            >
              {{ type.label }}
            </option>

          </select>

        </div>

      </div>

      <!-- ACTIONS -->

      <div class="form-actions">

        <button

          type="button"

          class="cancel-btn"

          @click="emit('close')"
        >
          Cancel
        </button>

        <button

          type="button"

          class="save-btn"

          :disabled="saving"

          @click="submitSport"
        >

          <i
            v-if="saving"
            class="fa-solid fa-spinner fa-spin"
          ></i>

          <i
            v-else
            class="fa-solid fa-plus"
          ></i>

          {{ saving ? 'Saving...' : 'Add Sport' }}

        </button>

      </div>

    </div>

  </div>

</template>

<style scoped>
.modal-overlay {

  position: fixed;

  inset: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 1rem;

  background: rgba(0, 0, 0, 0.45);

  z-index: 1000;
}

.sport-form-modal {

  width: 100%;

  max-width: 520px;

  display: flex;

  flex-direction: column;

  gap: 1.5rem;

  padding: 1.5rem;

  border-radius: 18px;

  background: white;
}

.form-header {

  display: flex;

  align-items: flex-start;

  justify-content: space-between;
}

.form-header h2 {

  margin: 0;
}

.form-header p {

  margin-top: 0.35rem;

  color: #6b7280;
}

.close-btn {

  border: none;

  background: transparent;

  font-size: 1.1rem;

  cursor: pointer;
}

.active-event-banner {

  display: flex;

  align-items: center;

  gap: 0.75rem;

  padding: 0.9rem 1rem;

  border-radius: 12px;

  background: #eff6ff;

  color: #1d4ed8;

  font-weight: 600;
}

.form-body {

  display: flex;

  flex-direction: column;

  gap: 1rem;
}

.form-group {

  display: flex;

  flex-direction: column;

  gap: 0.45rem;
}

.form-group label {

  font-weight: 600;
}

.form-input {

  padding: 0.85rem 1rem;

  border: 1px solid #d1d5db;

  border-radius: 10px;

  outline: none;
}

.form-input:focus {

  border-color: #2563eb;
}

.form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 0.75rem;
}

.cancel-btn,
.save-btn {

  display: flex;

  align-items: center;

  gap: 0.5rem;

  padding: 0.8rem 1rem;

  border: none;

  border-radius: 10px;

  cursor: pointer;

  transition: 0.2s ease;
}

.cancel-btn {

  background: #f3f4f6;
}

.save-btn {

  background: #2563eb;

  color: white;
}

.save-btn:hover {

  background: #1d4ed8;
}

.save-btn:disabled {

  opacity: 0.7;

  cursor: not-allowed;
}
</style>