# NEST

NEST - or **'Nava Service Tracking'** - is a library that supports creations, changes, deletions, and updates to service plans. This is just for pure processing, not about communication with users about their actions.

---

## What are service plans?

Service plans, put simply, are templates of tasks - in a hierarchical format - that defines the likely tasks for serving that client _'The Nava Way'_. In other words, service plans are a non-exhaustive list of tasks that must be checked (TRUE or FALSE) against.

---

### **Job 1 [Create]**

- Create Service Plan

### **Job 2 [Delete]**

- Delete Service Plan

### **Job 3 [Read, Update]**

- Refactor Service Plan
  - Basically, we would want to re-build the service plan within the app, query the existing service plan from Airtable, compare the two plans together, add necessary items and then delete unnecessary items.
  - Necessary = Buckets, Milestones, & Tasks that exist in the re-built service plan but not the existing service plan.
  - Unnecessary = Buckets, Milestones, & Tasks that exist in the current service plan but not the re-built service plan.
  - **Note**: we don't want to delete the whole thing and then re-create because we do not wan't to delete all existing work.
    - ex: a service plan needs to be re-factored in the middle of a service journey. well, we don't want to delete everything that they have completed, as the service team is probably thinking about how

### **Job 4 [Read, Update]**

- Update Changes Across Service Plan for All Created Service Plans
  - Job 1:
    - Apply new buckets / milestones / tasks to the existing service plans where applicable
      - How do we do this?
        1. Can only update by group_size at a given time (ex: Large Group)
      - Approach: do not change items that have been completed or deleted (historical), change forward looking / incomplete items only
  - Job 2:
    - Apply removed / deleted buckets / milestones / tasks to the existing service plans
      - Need to think about this one more
      - Approach: do not change items that are completed / are in the past
